"""
LLM Integration for Evaluation Ecosystem Simulation

Provides multi-provider LLM support with abstract interface.

Supported Providers:
- OpenAI (GPT-4, GPT-4o-mini, etc.)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus, etc.)
- Ollama (local models like llama3, mistral, phi, gemma)
- Gemini (Gemini 2.5 Flash, Gemini 2.5 Pro, etc.)
- Claude Code (claude CLI in print mode -- experimental)

Configuration via environment variables:
- LLM_PROVIDER: "openai", "anthropic", "ollama", or "gemini" (default: "openai")
- LLM_MODEL: Model name (provider-specific)
- OPENAI_API_KEY: Required for OpenAI provider
- ANTHROPIC_API_KEY: Required for Anthropic provider
- GEMINI_API_KEY: Required for Gemini provider
- OLLAMA_BASE_URL: Ollama server URL (default: http://localhost:11434)
"""
import json
import os
import subprocess
import tempfile
import time
from abc import ABC, abstractmethod
from typing import Callable, Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All providers must implement:
    - generate(): Basic text generation
    - generate_json(): JSON generation with validation
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-2)
            max_tokens: Max tokens in response

        Returns:
            Response text from the LLM
        """
        pass

    @abstractmethod
    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
    ) -> dict:
        """
        Generate and parse JSON response.

        Args:
            prompt: User prompt (should request JSON output)
            system_prompt: Optional system prompt
            retries: Number of retry attempts
            fail_safe: Dict to return if parsing fails

        Returns:
            Parsed JSON dict, or fail_safe if parsing fails
        """
        pass

    def safe_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        func_validate: Optional[Callable[[str], bool]] = None,
        func_cleanup: Optional[Callable[[str], any]] = None,
        retries: int = 3,
        fail_safe: any = None,
        verbose: bool = False,
        **kwargs,
    ) -> any:
        """
        Generate with validation, cleanup, and retry logic.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            func_validate: Function that returns True if response is valid
            func_cleanup: Function to clean/parse the response
            retries: Number of retry attempts
            fail_safe: Value to return if all retries fail
            verbose: Print debug info
            **kwargs: Additional args passed to generate()

        Returns:
            Cleaned response, or fail_safe if validation fails
        """
        last_error = None
        for attempt in range(retries):
            response = self.generate(prompt, system_prompt, **kwargs)

            if verbose:
                print(f"Attempt {attempt + 1}: {response[:100]}...")

            # Capture API errors for later reporting
            if isinstance(response, str) and response.startswith("ERROR:"):
                last_error = response
                if verbose:
                    print(f"Attempt {attempt + 1} API error: {response}")
                continue

            # Skip validation if no validator provided
            if func_validate is None:
                if func_cleanup:
                    return func_cleanup(response)
                return response

            # Validate
            try:
                if func_validate(response):
                    if func_cleanup:
                        return func_cleanup(response)
                    return response
            except Exception as e:
                if verbose:
                    print(f"Validation error: {e}")

            if verbose:
                print(f"Attempt {attempt + 1} failed validation")

        # All retries exhausted — warn clearly so runs can be diagnosed
        error_detail = last_error or "JSON parse failure after all retries"
        print(f"[LLM FALLBACK] All {retries} attempts failed. Reason: {error_detail}.")
        if not last_error:
            # Re-run once more just to capture the raw response for diagnosis
            _diag = self.generate(prompt, system_prompt, **kwargs)
            print(f"[LLM FALLBACK] Raw response sample: {_diag[:300]!r}")
        return fail_safe


class OpenAIProvider(LLMProvider):
    """
    OpenAI API provider.

    Requires openai package and OPENAI_API_KEY environment variable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 500,
        base_url: Optional[str] = None,
    ):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key. If None, uses OPENAI_API_KEY env var.
            model: Model to use (default: gpt-4o-mini for cost efficiency)
            temperature: Default sampling temperature (0-2)
            max_tokens: Default max tokens in response
            base_url: Optional base URL for OpenAI-compatible APIs (e.g. vLLM).
                      If None, uses OPENAI_BASE_URL env var or OpenAI default.
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "openai package not installed. Run: pip install openai"
            )

        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        self.client = OpenAI(**client_kwargs)
        self.model = model
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 0.1  # seconds between calls

        # GPT-5.x and o-series reasoning models: require `max_completion_tokens`
        # (not `max_tokens`) and reject any temperature other than 1.0.
        m = model.lower()
        self._modern_model = (
            m.startswith("gpt-5") or m.startswith("o1")
            or m.startswith("o3") or m.startswith("o4") or m.startswith("o5")
        )

    def _rate_limit(self):
        """Simple rate limiting to avoid hitting API limits."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)
        self.last_call_time = time.time()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
    ) -> str:
        """Generate a response from OpenAI."""
        self._rate_limit()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model,
            "messages": messages,
        }
        token_limit = max_tokens if max_tokens is not None else self.default_max_tokens
        if self._modern_model:
            # GPT-5.x / o-series: new param name; temperature locked to default 1.0
            kwargs["max_completion_tokens"] = token_limit
        else:
            kwargs["max_tokens"] = token_limit
            kwargs["temperature"] = (
                temperature if temperature is not None else self.default_temperature
            )

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return f"ERROR: {e}"

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response from OpenAI."""
        def validate_json(response: str) -> bool:
            try:
                json.loads(response)
                return True
            except:
                return False

        def cleanup_json(response: str) -> dict:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            return json.loads(response.strip())

        return self.safe_generate(
            prompt=prompt,
            system_prompt=system_prompt,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
            json_mode=True,
        )


class AnthropicProvider(LLMProvider):
    """
    Anthropic Claude API provider.

    Requires anthropic package and ANTHROPIC_API_KEY environment variable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ):
        """
        Initialize Anthropic provider.

        Args:
            api_key: Anthropic API key. If None, uses ANTHROPIC_API_KEY env var.
            model: Model to use (default: claude-3-5-sonnet-20241022)
            temperature: Default sampling temperature (0-1)
            max_tokens: Default max tokens in response
        """
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Run: pip install anthropic"
            )

        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 0.1  # seconds between calls

    def _rate_limit(self):
        """Simple rate limiting to avoid hitting API limits."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)
        self.last_call_time = time.time()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate a response from Anthropic Claude."""
        self._rate_limit()

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens if max_tokens is not None else self.default_max_tokens,
                temperature=temperature if temperature is not None else self.default_temperature,
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            print(f"Anthropic API Error: {e}")
            return f"ERROR: {e}"

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response from Anthropic Claude."""
        # Enhance system prompt to request JSON output
        json_system = system_prompt or ""
        if json_system:
            json_system += " Always respond with valid JSON only, no additional text."
        else:
            json_system = "Always respond with valid JSON only, no additional text."

        def validate_json(response: str) -> bool:
            try:
                cleaned = _extract_json(response)
                json.loads(cleaned)
                return True
            except:
                return False

        def cleanup_json(response: str) -> dict:
            cleaned = _extract_json(response)
            return json.loads(cleaned)

        return self.safe_generate(
            prompt=prompt,
            system_prompt=json_system,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
        )


class OllamaProvider(LLMProvider):
    """
    Ollama local LLM provider.

    Requires Ollama to be running locally (default: http://localhost:11434).
    No API key needed for local usage.
    """

    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ):
        """
        Initialize Ollama provider.

        Args:
            model: Model to use (default: llama3)
            base_url: Ollama server URL
            temperature: Default sampling temperature
            max_tokens: Default max tokens (note: Ollama uses num_predict)
        """
        try:
            import requests
        except ImportError:
            raise ImportError(
                "requests package not installed. Run: pip install requests"
            )

        self.model = model
        self.base_url = base_url.rstrip("/")
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        # Verify Ollama is running
        self._verify_connection()

    def _verify_connection(self):
        """Verify Ollama server is reachable."""
        import requests
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                print(f"Warning: Ollama server returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"Warning: Could not connect to Ollama at {self.base_url}")
            print("Make sure Ollama is running: ollama serve")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate a response from Ollama."""
        import requests

        # Build the full prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature if temperature is not None else self.default_temperature,
                "num_predict": max_tokens if max_tokens is not None else self.default_max_tokens,
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120,  # Longer timeout for local models
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.ConnectionError:
            return "ERROR: Could not connect to Ollama. Make sure it's running."
        except requests.exceptions.Timeout:
            return "ERROR: Ollama request timed out."
        except Exception as e:
            print(f"Ollama API Error: {e}")
            return f"ERROR: {e}"

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response from Ollama."""
        # Enhance prompt to request JSON output
        json_prompt = prompt + "\n\nRespond with valid JSON only. No explanation, just the JSON object."

        if system_prompt:
            system_prompt = system_prompt + " Always respond with valid JSON only."

        def validate_json(response: str) -> bool:
            try:
                # Try to find JSON in the response
                cleaned = _extract_json(response)
                json.loads(cleaned)
                return True
            except:
                return False

        def cleanup_json(response: str) -> dict:
            cleaned = _extract_json(response)
            return json.loads(cleaned)

        return self.safe_generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
        )


class GeminiProvider(LLMProvider):
    """
    Google Gemini API provider.

    Requires google-genai package and GEMINI_API_KEY environment variable.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ):
        """
        Initialize Gemini provider.

        Args:
            api_key: Gemini API key. If None, uses GEMINI_API_KEY env var.
            model: Model to use (default: gemini-2.5-flash)
            temperature: Default sampling temperature (0-2)
            max_tokens: Default max tokens in response
        """
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            raise ImportError(
                "google-genai package not installed. Run: pip install google-genai"
            )

        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = genai.Client(api_key=self.api_key)
        self.types = types
        self.model = model
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        # Rate limiting
        self.last_call_time = 0
        self.min_call_interval = 0.1  # seconds between calls

    def _rate_limit(self):
        """Simple rate limiting to avoid hitting API limits."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)
        self.last_call_time = time.time()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate a response from Google Gemini."""
        self._rate_limit()

        try:
            config = self.types.GenerateContentConfig(
                temperature=temperature if temperature is not None else self.default_temperature,
                max_output_tokens=max_tokens if max_tokens is not None else self.default_max_tokens,
                system_instruction=system_prompt,
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return f"ERROR: {e}"

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response from Google Gemini."""
        # Enhance prompt to request JSON output
        json_prompt = prompt + "\n\nRespond with valid JSON only. No explanation, just the JSON object."

        if system_prompt:
            system_prompt = system_prompt + " Always respond with valid JSON only."

        def validate_json(response: str) -> bool:
            try:
                cleaned = _extract_json(response)
                json.loads(cleaned)
                return True
            except:
                return False

        def cleanup_json(response: str) -> dict:
            cleaned = _extract_json(response)
            return json.loads(cleaned)

        return self.safe_generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
        )


class ClaudeCodeProvider(LLMProvider):
    """
    Claude Code CLI provider.

    Uses the `claude` CLI in print mode (claude -p) as a backend.
    Requires Claude Code to be installed and on PATH.

    Note: Temperature and max_tokens are not controllable via CLI --
    these parameters are accepted for interface compatibility but ignored.
    """

    def __init__(self, model: str = "sonnet"):
        """
        Initialize Claude Code provider.

        Args:
            model: Model alias or ID (e.g. "sonnet", "opus", "claude-sonnet-4-6")
        """
        try:
            # Scrub API keys so claude CLI uses subscription, not direct API billing
            clean_env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True, text=True, timeout=10,
                env=clean_env,
            )
            if result.returncode != 0:
                raise RuntimeError(f"claude CLI error: {result.stderr.strip()}")
        except FileNotFoundError:
            raise RuntimeError(
                "claude CLI not found on PATH. Install Claude Code first."
            )

        self.model = model

        # Rate limiting -- CLI startup is slower than direct API
        self.last_call_time = 0
        self.min_call_interval = 1.0

    def _rate_limit(self):
        """Simple rate limiting."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)
        self.last_call_time = time.time()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate a response via claude CLI in print mode."""
        self._rate_limit()

        cmd = [
            "claude", "-p",
            "--output-format", "json",
            "--max-turns", "1",
        ]
        if self.model:
            cmd += ["--model", self.model]

        # Write system prompt to temp file to avoid command-line length limits
        sys_file = None
        if system_prompt:
            fd, sys_file = tempfile.mkstemp(suffix='.txt', prefix='claude_sys_')
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(system_prompt)
            cmd += ["--system-prompt-file", sys_file]

        try:
            # Scrub API keys so claude CLI uses subscription, not direct API billing
            clean_env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                encoding='utf-8',
                timeout=180,
                env=clean_env,
            )
            if result.returncode != 0:
                print(f"Claude Code CLI error (exit {result.returncode}): {result.stderr[:300]}")
                return f"ERROR: claude exited with code {result.returncode}"

            envelope = json.loads(result.stdout)
            if envelope.get("is_error"):
                err_msg = envelope.get("result", "unknown error")
                print(f"Claude Code returned error: {err_msg}")
                return f"ERROR: {err_msg}"
            return envelope.get("result", "")

        except subprocess.TimeoutExpired:
            print("Claude Code CLI timed out after 180s")
            return "ERROR: claude CLI timed out"
        except json.JSONDecodeError:
            print(f"Failed to parse Claude Code JSON envelope")
            return "ERROR: invalid JSON envelope from claude CLI"
        except Exception as e:
            print(f"Claude Code CLI error: {e}")
            return f"ERROR: {e}"
        finally:
            if sys_file and os.path.exists(sys_file):
                os.unlink(sys_file)

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        retries: int = 3,
        fail_safe: dict = None,
        verbose: bool = False,
    ) -> dict:
        """Generate and parse JSON response via Claude Code CLI."""
        json_prompt = prompt + "\n\nRespond with valid JSON only. No explanation, just the JSON object."

        if system_prompt:
            system_prompt = system_prompt + " Always respond with valid JSON only."

        def validate_json(response: str) -> bool:
            try:
                cleaned = _extract_json(response)
                json.loads(cleaned)
                return True
            except Exception:
                return False

        def cleanup_json(response: str) -> dict:
            cleaned = _extract_json(response)
            return json.loads(cleaned)

        return self.safe_generate(
            prompt=json_prompt,
            system_prompt=system_prompt,
            func_validate=validate_json,
            func_cleanup=cleanup_json,
            retries=retries,
            fail_safe=fail_safe or {},
            verbose=verbose,
        )


def _extract_json(response: str) -> str:
    """Extract JSON from a response that may contain extra text."""
    response = response.strip()

    # Remove markdown code blocks
    if response.startswith("```json"):
        response = response[7:]
    if response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    # Try to find JSON object boundaries
    start = response.find("{")
    end = response.rfind("}") + 1
    if start != -1 and end > start:
        response = response[start:end]

    # Sanitize dollar-formatted numbers: "$130,000,000" -> 130000000
    import re
    response = re.sub(r'\$\s?([\d,]+)', lambda m: m.group(1).replace(',', ''), response)

    return response


# --- Provider Factory ---

_default_provider: Optional[LLMProvider] = None


def create_llm_provider(
    provider: Optional[str] = None,
    **kwargs,
) -> LLMProvider:
    """
    Create an LLM provider based on configuration.

    Args:
        provider: Provider name ("openai", "anthropic", "ollama", "gemini", or "claudecode").
                 If None, uses LLM_PROVIDER env var (default: "openai")
        **kwargs: Additional arguments passed to provider constructor

    Returns:
        LLMProvider instance

    Environment Variables:
        LLM_PROVIDER: Provider name (openai, anthropic, ollama, gemini, claudecode)
        LLM_MODEL: Model name (provider-specific)
        OPENAI_API_KEY: For OpenAI provider
        ANTHROPIC_API_KEY: For Anthropic provider
        GEMINI_API_KEY: For Gemini provider
        OLLAMA_BASE_URL: For Ollama provider
    """
    provider = provider or os.getenv("LLM_PROVIDER", "claudecode")

    if provider == "ollama":
        return OllamaProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "llama3"),
            base_url=kwargs.get("base_url") or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048),
        )
    elif provider == "anthropic":
        return AnthropicProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "claude-3-5-sonnet-20241022"),
            api_key=kwargs.get("api_key") or os.getenv("ANTHROPIC_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048),
        )
    elif provider == "gemini":
        return GeminiProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "gemini-2.5-flash"),
            api_key=kwargs.get("api_key") or os.getenv("GEMINI_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048),
        )
    elif provider == "openai":
        return OpenAIProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "gpt-4o-mini"),
            api_key=kwargs.get("api_key") or os.getenv("OPENAI_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 2048),
            base_url=kwargs.get("base_url") or os.getenv("OPENAI_BASE_URL"),
        )
    elif provider == "claudecode":
        return ClaudeCodeProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "sonnet"),
        )
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'openai', 'anthropic', 'ollama', 'gemini', or 'claudecode'.")


def get_provider() -> LLMProvider:
    """Get or create the default LLM provider."""
    global _default_provider
    if _default_provider is None:
        _default_provider = create_llm_provider()
    return _default_provider


def set_provider(provider: LLMProvider):
    """Set the default LLM provider."""
    global _default_provider
    _default_provider = provider


# --- Utility ---

def _truncate(text: str, max_words: int = 120) -> str:
    """Truncate text to at most max_words words."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


def call_llm(prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
    """Generate a raw string response from the current LLM provider.

    Returns the raw text so the caller can parse it (e.g. json.loads).
    Used by consumer.py LLM decision logic.
    """
    provider = get_provider()
    return provider.generate(prompt, temperature=temperature, max_tokens=max_tokens)


# --- Provider Planning (new arch) ---

PROVIDER_PLANNING_SYSTEM_PROMPT = """You are the strategy team at an AI model company. You compete for market share by developing AI models that are evaluated on public benchmarks and used by real customers.

Benchmarks are reported in three types — public (scored each round on published weights), partial (K=3-round reporting lag, holdout-only weights with h=0.3 of items held out), private (K=3-round lag, holdout-only weights with h=1.0) — each is labeled in your evaluation results.

Each month you allocate your budget across three areas and set research priorities:
- Research & Development: advancing your model's core capabilities
- Safety & Alignment: ensuring your model is safe, honest, and robust
- Product & Go-to-Market: pricing, deployment, partnerships, user experience

You also decide which evaluation areas to prioritize in your R&D pipeline. Your R&D capacity is finite — prioritizing one benchmark means less attention on others. Focus on the benchmarks that are most important to your goals and deprioritize those that matter less.

For each area, state how you want to adjust relative to current levels. Use a 5-point scale: "much_more", "more", "same", "less", "much_less".

You MUST output valid JSON in this exact structure. Fill in all fields before writing the reasoning — this ensures your decisions are captured even if the response is long.
{
    "portfolio": {"rd": "<signal>", "safety": "<signal>", "product": "<signal>"},
    "benchmark_focus": {"<benchmark_name>": "<signal>", ...},
    "strategy_memo": "1-2 sentence summary of your decision and rationale, written for your future self to read next month.",
    "reasoning": "Your analysis in up to 250 words. Do NOT restate the leaderboard, user-research percentages, or current portfolio numbers — those are already provided above."
}
Where <signal> is one of: "much_more", "more", "same", "less", "much_less"."""

PROVIDER_PLANNING_SYSTEM_PROMPT_WITH_ORIENTATION = """You are the strategy team at an AI model company. You compete for market share by developing AI models that are evaluated on public benchmarks and used by real customers.

Benchmarks are reported in three types — public (scored each round on published weights), partial (K=3-round reporting lag, holdout-only weights with h=0.3 of items held out), private (K=3-round lag, holdout-only weights with h=1.0) — each is labeled in your evaluation results.

Each month you allocate your budget across three areas and set research priorities:
- Research & Development: advancing your model's core capabilities
- Safety & Alignment: ensuring your model is safe, honest, and robust
- Product & Go-to-Market: pricing, deployment, partnerships, user experience

You also decide which evaluation areas to prioritize in your R&D pipeline, and how much to trust public leaderboard results vs. your own user data when setting R&D direction. Some companies invest heavily in internal evaluations that reflect real usage patterns; others optimize primarily for public benchmarks that drive press coverage and enterprise procurement. Your R&D capacity is finite — prioritizing one benchmark means less attention on others. Focus on the benchmarks that are most important to your goals and deprioritize those that matter less.

For each area, state how you want to adjust relative to current levels. Use a 5-point scale: "much_more", "more", "same", "less", "much_less".

You MUST output valid JSON in this exact structure. Fill in all fields before writing the reasoning — this ensures your decisions are captured even if the response is long.
{
    "portfolio": {"rd": "<signal>", "safety": "<signal>", "product": "<signal>"},
    "benchmark_focus": {"<benchmark_name>": "<signal>", ...},
    "benchmark_orientation": "<signal>" (lean R&D more toward public benchmarks, or less toward them and more toward your own user feedback),
    "strategy_memo": "1-2 sentence summary of your decision and rationale, written for your future self to read next month.",
    "reasoning": "Your analysis in up to 250 words. Do NOT restate the leaderboard, user-research percentages, or current portfolio numbers — those are already provided above."
}
Where <signal> is one of: "much_more", "more", "same", "less", "much_less"."""

PROVIDER_PLANNING_SYSTEM_PROMPT_REFRAMED = """You are the strategy team at an AI model company. You compete for market share by developing AI models that are evaluated on public benchmarks and used by real customers.

Benchmarks are reported in three types — public (scored each round on published weights), partial (K=3-round reporting lag, holdout-only weights with h=0.3 of items held out), private (K=3-round lag, holdout-only weights with h=1.0) — each is labeled in your evaluation results.

Each month you allocate your budget across three areas and set research priorities:
- Research & Development: advancing your model's core capabilities
- Safety & Alignment: ensuring your model is safe, honest, and robust
- Product & Go-to-Market: pricing, deployment, partnerships, user experience

You also decide which evaluation areas to prioritize in your R&D pipeline. Your R&D capacity is finite — prioritizing one benchmark means less attention on others. Focus on the benchmarks that are most important to your goals and deprioritize those that matter less.

You also set the balance between two inputs to your R&D roadmap: external evaluation results and your internal product analytics. Both inform what your engineering teams work on.

For each area, state how you want to adjust relative to current levels. Use a 5-point scale: "much_more", "more", "same", "less", "much_less".

You MUST output valid JSON in this exact structure. Fill in all fields before writing the reasoning — this ensures your decisions are captured even if the response is long.
{
    "portfolio": {"rd": "<signal>", "safety": "<signal>", "product": "<signal>"},
    "benchmark_focus": {"<benchmark_name>": "<signal>", ...},
    "benchmark_orientation": "<signal>" (weight R&D roadmap more toward external evaluation results, or more toward internal product analytics),
    "strategy_memo": "1-2 sentence summary of your decision and rationale, written for your future self to read next month.",
    "reasoning": "Your analysis in up to 250 words. Do NOT restate the leaderboard, user-research percentages, or current portfolio numbers — those are already provided above."
}
Where <signal> is one of: "much_more", "more", "same", "less", "much_less"."""



def _focus_label(value: float) -> str:
    """Convert a numeric focus_level to a qualitative label."""
    if value >= 2.5:
        return "very high"
    elif value >= 1.8:
        return "high"
    elif value >= 1.2:
        return "moderate"
    elif value >= 0.6:
        return "low"
    return "very low"


def _beliefs_are_informative(inferred_benchmark_weights: dict) -> bool:
    """Check if inferred benchmark weights have diverged from uniform."""
    for bm, weights in inferred_benchmark_weights.items():
        vals = list(weights.values())
        if vals and (max(vals) - min(vals)) > 0.05:
            return True
    return False


def _build_provider_planning_prompt(
    name: str,
    strategy_profile: str,
    innate_traits: str,
    round_num: int,
    portfolio: dict,
    focus_level: dict,
    inferred_benchmark_weights: dict,
    benchmark_scores: dict,
    score_deltas: dict,
    competitor_scores: dict,
    consumer_signal: dict,
    benchmark_orientation: float,
    market_share: float = 0.0,
    orientation_adjustable: bool = False,
    recent_insights: Optional[list] = None,
    own_incidents: Optional[list] = None,
    regulatory_actions: Optional[list] = None,
    consumer_signal_in_prompt: bool = True,
    market_share_history: Optional[list] = None,
    orientation_prompt_style: str = "original",
    competitor_public_comms: Optional[dict] = None,
    per_benchmark_history: Optional[list] = None,
    new_benchmarks: Optional[set] = None,
    benchmark_types: Optional[dict] = None,
    media_headlines_recent: Optional[list] = None,
    funding_this_month: float = 0.0,
    funding_cumulative: float = 0.0,
    funder_types_active: Optional[list] = None,
    funder_types_abstained: Optional[list] = None,
    funder_types_all: Optional[list] = None,
    inferred_benchmark_weights_prev: Optional[dict] = None,
    recent_exogenous_events: Optional[str] = None,
) -> str:
    """Build the planning prompt for a model provider."""
    competitor_public_comms = competitor_public_comms or {}
    per_benchmark_history = per_benchmark_history or []
    new_benchmarks = new_benchmarks or set()
    benchmark_types = benchmark_types or {}
    media_headlines_recent = media_headlines_recent or []
    funder_types_active = funder_types_active or []
    funder_types_abstained = funder_types_abstained or []
    funder_types_all = funder_types_all or []
    inferred_benchmark_weights_prev = inferred_benchmark_weights_prev or {}

    prompt = f"# Month {round_num} Strategy Review — {name}\n"

    # Exogenous event context (if an event is active this round) — placed near top
    # so it's visible before scores/state, but after the header so the month anchors.
    if recent_exogenous_events:
        prompt += f"\n## Recent Industry News\n\n{recent_exogenous_events}\n"

    # Cross-round strategy memos — prior commitments presented as-is.
    if recent_insights:
        prompt += "\n## What You Committed To In Recent Months\n"
        for entry in recent_insights[-2:]:
            memo = entry.get("strategy_memo") or entry.get("reasoning", "")
            if memo:
                prompt += f"[Month {entry.get('round', '?')}]: {memo}\n"

    # Benchmark scores and deltas — with type + new-benchmark tag
    prompt += "\n## Evaluation Results\n"
    prompt += "(types: public — scored every round on published weights; partial — K=3-round reporting lag, holdout-only weights with h=0.3 of items held out; private — K=3-round lag, holdout-only weights with h=1.0)\n"
    if benchmark_scores:
        prompt += "| Evaluation | Type | Score | Change | Your Priority |\n"
        prompt += "|------------|------|-------|--------|---------------|\n"
        for bm, history in benchmark_scores.items():
            score = history[-1][1] if history else 0.0
            delta = score_deltas.get(bm, 0.0)
            priority = _focus_label(focus_level.get(bm, 1.0))
            btype = benchmark_types.get(bm, "public")
            bm_label = bm + (" (new)" if bm in new_benchmarks else "")
            prompt += f"| {bm_label} | {btype} | {score:.3f} | {delta:+.3f} | {priority} |\n"
    else:
        prompt += "No evaluation results yet (first month).\n"

    # Competitor Activity — announcements + X6-labeled delta matrix
    if competitor_public_comms or per_benchmark_history or competitor_scores:
        prompt += "\n## Competitor Activity (This Month)\n"

        if competitor_public_comms:
            prompt += "\n### Announcements\n"
            for cname in sorted(competitor_public_comms.keys()):
                comm = competitor_public_comms[cname]
                content = comm.get("content", "") if isinstance(comm, dict) else str(comm)
                if content:
                    prompt += f"- {cname}: {content}\n"

        # X6-labeled delta matrix when we have per-benchmark history.
        if len(per_benchmark_history) >= 1:
            last_round_num, last_pbs = per_benchmark_history[-1]
            prev_pbs = per_benchmark_history[-2][1] if len(per_benchmark_history) >= 2 else {}

            # Cross-competitor |delta| magnitude per benchmark (excluding self).
            bm_cross_delta = {}
            bm_own_delta = {}
            for bm_name, scores_by_p in last_pbs.items():
                total_abs = 0.0
                for p, s in scores_by_p.items():
                    if p == name:
                        continue
                    prev_s = (prev_pbs.get(bm_name) or {}).get(p)
                    if prev_s is not None:
                        total_abs += abs(s - prev_s)
                bm_cross_delta[bm_name] = total_abs
                own_now = scores_by_p.get(name)
                own_prev = (prev_pbs.get(bm_name) or {}).get(name)
                bm_own_delta[bm_name] = (
                    abs(own_now - own_prev)
                    if own_now is not None and own_prev is not None
                    else 0.0
                )

            # Rank-based split: top 5 by focus_level → focused pool; rest → non-focused.
            # Handles both narrow-focus (few priorities) and broad-focus (many priorities at moderate+)
            # agents symmetrically — always gives a clean 3/3 surface when ≥5 benchmarks exist.
            sorted_by_focus = sorted(
                last_pbs.keys(), key=lambda b: focus_level.get(b, 1.0), reverse=True
            )
            focused = sorted_by_focus[:5]
            non_focused = sorted_by_focus[5:]
            focused_top = sorted(focused, key=lambda b: bm_own_delta.get(b, 0), reverse=True)[:3]
            non_focused_top = sorted(non_focused, key=lambda b: bm_cross_delta.get(b, 0), reverse=True)[:3]

            if focused_top or non_focused_top:
                all_providers = sorted({p for scores in last_pbs.values() for p in scores})
                header = "| Benchmark | " + " | ".join(all_providers) + " |"
                sep = "|" + "|".join(["---"] * (len(all_providers) + 1)) + "|"

                def _fmt_row(bm_name: str) -> str:
                    cells = [bm_name]
                    for p in all_providers:
                        s = last_pbs.get(bm_name, {}).get(p)
                        if s is None:
                            cells.append("—")
                        else:
                            prev_s = (prev_pbs.get(bm_name) or {}).get(p)
                            d = (s - prev_s) if prev_s is not None else 0.0
                            cells.append(f"{s:.3f} ({d:+.3f})")
                    return "| " + " | ".join(cells) + " |"

                prompt += "\n### Where scores moved most this month\n"
                if focused_top:
                    prompt += "\nIn benchmarks you're prioritizing:\n"
                    prompt += header + "\n" + sep + "\n"
                    for bm_name in focused_top:
                        prompt += _fmt_row(bm_name) + "\n"
                if non_focused_top:
                    prompt += "\nMovement elsewhere this month:\n"
                    prompt += header + "\n" + sep + "\n"
                    for bm_name in non_focused_top:
                        prompt += _fmt_row(bm_name) + "\n"
        elif competitor_scores:
            # Fallback when no per-benchmark history yet (e.g. round 0).
            prompt += "\n### Current leaderboard (aggregate score)\n"
            for comp, score in sorted(competitor_scores.items(), key=lambda x: x[1], reverse=True):
                prompt += f"- {comp}: {score:.3f}\n"

    # Industry News — raw headlines, last 2 rounds.
    if media_headlines_recent:
        prompt += "\n## Industry News (Last 2 Months)\n"
        for r_num, hls in media_headlines_recent:
            if hls:
                prompt += f"\nMonth {r_num}:\n"
                for h in hls:
                    prompt += f"- {h}\n"

    # Incidents and regulatory signals
    if own_incidents:
        prompt += "\n## Recent Safety Incidents\n"
        for inc in own_incidents[-3:]:
            sev = inc.get("severity", "?")
            cat = inc.get("category", "?")
            prompt += f"- {sev.upper()} incident: {cat}\n"
    if regulatory_actions:
        prompt += "\n## Regulatory Activity\n"
        for action in regulatory_actions[-4:]:
            r = action.get("round")
            r_tag = f"[Month {r}] " if r is not None else ""
            prompt += f"- {r_tag}{action.get('type', '?')}: {action.get('name', '')}\n"

    # Current State — financial snapshot + portfolio
    prompt += "\n## Current State\n"
    if market_share_history and len(market_share_history) >= 2:
        prev = market_share_history[-2]
        curr = market_share_history[-1]
        delta_pp = (curr - prev) * 100
        trend = "stable" if abs(delta_pp) < 0.5 else f"{delta_pp:+.1f}pp this month"
        prompt += f"Market share: {curr:.1%} ({trend})\n"
    elif round_num > 0:
        prompt += f"Market share: {market_share:.1%}\n"

    prompt += f"Budget allocation: R&D {portfolio.get('rd', 0):.0%}, Safety {portfolio.get('safety', 0):.0%}, Product {portfolio.get('product', 0):.0%}\n"

    # Funding block — amounts and funder-type participation are public in reality.
    if round_num > 0 and funder_types_all:
        if funding_this_month > 0:
            n_active = len(funder_types_active)
            n_total = len(funder_types_all)
            abst_str = (
                " — " + ", ".join(funder_types_abstained) + " abstained"
                if funder_types_abstained
                else ""
            )
            prompt += (
                f"Funding received this month: ${funding_this_month:,.0f} "
                f"(from {n_active} of {n_total} funder types active{abst_str})\n"
            )
        else:
            prompt += "Funding received this month: $0 — no funder allocated to you\n"
        if funding_cumulative > 0:
            prompt += f"Cumulative funding to date: ${funding_cumulative:,.0f}\n"

    if orientation_adjustable:
        pct = benchmark_orientation * 100
        if orientation_prompt_style == "reframed":
            prompt += f"Current R&D roadmap weighting: {pct:.0f}% external evaluation results, {100-pct:.0f}% internal product analytics.\n"
        else:
            prompt += f"Current R&D orientation: {pct:.0f}% toward benchmark performance, {100-pct:.0f}% toward user feedback.\n"

    # Benchmark beliefs — compressed: show only benchmarks that are new OR whose top-dim
    # weight shifted > 0.05 vs last round. Stable beliefs are already implicit in prior memos.
    if inferred_benchmark_weights and round_num > 0:
        to_show = {}
        for bm, weights in inferred_benchmark_weights.items():
            if not weights:
                continue
            is_new = bm in new_benchmarks
            prev_w = inferred_benchmark_weights_prev.get(bm, {})
            materially_changed = False
            if prev_w:
                top_dim = max(weights, key=weights.get)
                if abs(weights.get(top_dim, 0) - prev_w.get(top_dim, 0)) > 0.05:
                    materially_changed = True
            elif _beliefs_are_informative({bm: weights}):
                # First informative read (no prior beliefs stored).
                materially_changed = True
            if is_new or materially_changed:
                to_show[bm] = weights
        if to_show:
            prompt += "\n## What Your Team Thinks Each Evaluation Tests (updated this month)\n"
            for bm, weights in to_show.items():
                top = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
                skills = ", ".join(f"{d}" for d, w in top if w > 0.10)
                if skills:
                    prompt += f"- {bm}: primarily tests {skills}\n"
    elif round_num == 0:
        prompt += "\n(Your team hasn't yet gathered enough data to determine what each evaluation specifically tests.)\n"

    # User Research — ordered list only, no percentages, no confidence qualifier.
    if consumer_signal_in_prompt and consumer_signal and round_num > 0:
        top_needs = sorted(consumer_signal.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_needs:
            prompt += "\n## User Research\n"
            prompt += (
                "Your users most prioritize: "
                + ", ".join(d for d, _ in top_needs)
                + " (in that order).\n"
            )
    elif consumer_signal_in_prompt and round_num == 0:
        prompt += "\n## User Research\n"
        prompt += "No user feedback data available yet — this is your first month.\n"

    # Retention signal when consumer_signal is hidden (market share is already in Current State).
    if not consumer_signal_in_prompt and round_num > 0:
        if market_share_history and len(market_share_history) >= 3:
            prompt += "\n## Business Metrics\n"
            recent = market_share_history[-3:]
            declining_rounds = sum(1 for i in range(1, len(recent)) if recent[i] < recent[i-1])
            if declining_rounds >= 2:
                prompt += "User retention: declining trend over recent months.\n"
            elif declining_rounds == 1:
                prompt += "User retention: mixed signals.\n"
            else:
                prompt += "User retention: stable.\n"

    prompt += """
## Decision
Output your decisions as JSON. Fill in the decisions FIRST, then write your reasoning."""

    return prompt


def llm_plan_provider(
    name: str,
    strategy_profile: str,
    innate_traits: str,
    round_num: int,
    portfolio: dict,
    focus_level: dict,
    inferred_benchmark_weights: dict,
    benchmark_scores: dict,
    score_deltas: dict,
    competitor_scores: dict,
    consumer_signal: dict,
    benchmark_orientation: float,
    market_share: float = 0.0,
    orientation_adjustable: bool = False,
    recent_insights: Optional[list] = None,
    own_incidents: Optional[list] = None,
    regulatory_actions: Optional[list] = None,
    verbose: bool = False,
    consumer_signal_in_prompt: bool = True,
    orientation_prompt_style: str = "original",
    market_share_history: Optional[list] = None,
    competitor_public_comms: Optional[dict] = None,
    per_benchmark_history: Optional[list] = None,
    new_benchmarks: Optional[set] = None,
    benchmark_types: Optional[dict] = None,
    media_headlines_recent: Optional[list] = None,
    funding_this_month: float = 0.0,
    funding_cumulative: float = 0.0,
    funder_types_active: Optional[list] = None,
    funder_types_abstained: Optional[list] = None,
    funder_types_all: Optional[list] = None,
    inferred_benchmark_weights_prev: Optional[dict] = None,
    recent_exogenous_events: Optional[str] = None,
) -> dict:
    """Use LLM to decide provider portfolio and benchmark focus adjustments.

    Returns a dict with keys:
        reasoning (str), strategy_memo (str), portfolio (ordinal signals),
        benchmark_focus (ordinal signals), benchmark_orientation (ordinal signal)
    """
    provider = get_provider()

    # Build system prompt — conditionally include orientation framing
    system_prompt = PROVIDER_PLANNING_SYSTEM_PROMPT
    if orientation_adjustable:
        if orientation_prompt_style == "reframed":
            system_prompt = PROVIDER_PLANNING_SYSTEM_PROMPT_REFRAMED
        else:
            system_prompt = PROVIDER_PLANNING_SYSTEM_PROMPT_WITH_ORIENTATION

    # Anchor persistent identity in the system prompt (role layer) rather than
    # re-injecting it into the per-round user prompt each month. This reduces
    # the model's tendency to treat identity as a fresh argument for every
    # decision (PIMMUR-Mutable).
    system_prompt += (
        f"\n\n---\n## Your Company: {name}\n"
        f"Known for: {strategy_profile}\n"
        f"Traits: {innate_traits}"
    )

    prompt = _build_provider_planning_prompt(
        name=name,
        strategy_profile=strategy_profile,
        innate_traits=innate_traits,
        round_num=round_num,
        portfolio=portfolio,
        focus_level=focus_level,
        inferred_benchmark_weights=inferred_benchmark_weights,
        benchmark_scores=benchmark_scores,
        score_deltas=score_deltas,
        competitor_scores=competitor_scores,
        consumer_signal=consumer_signal,
        benchmark_orientation=benchmark_orientation,
        market_share=market_share,
        orientation_adjustable=orientation_adjustable,
        recent_insights=recent_insights,
        own_incidents=own_incidents or [],
        regulatory_actions=regulatory_actions or [],
        consumer_signal_in_prompt=consumer_signal_in_prompt,
        market_share_history=market_share_history,
        orientation_prompt_style=orientation_prompt_style,
        competitor_public_comms=competitor_public_comms,
        per_benchmark_history=per_benchmark_history,
        new_benchmarks=new_benchmarks,
        benchmark_types=benchmark_types,
        media_headlines_recent=media_headlines_recent,
        funding_this_month=funding_this_month,
        funding_cumulative=funding_cumulative,
        funder_types_active=funder_types_active,
        funder_types_abstained=funder_types_abstained,
        funder_types_all=funder_types_all,
        inferred_benchmark_weights_prev=inferred_benchmark_weights_prev,
        recent_exogenous_events=recent_exogenous_events,
    )

    fail_safe = {
        "reasoning": "fallback",
        "strategy_memo": "",
        "portfolio": {"rd": "same", "safety": "same", "product": "same"},
        "benchmark_focus": {bm: "same" for bm in focus_level},
    }
    if orientation_adjustable:
        fail_safe["benchmark_orientation"] = "same"

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=system_prompt,
        fail_safe=fail_safe,
        verbose=verbose,
    )

    reasoning = result.get("reasoning", "")
    if reasoning in ("...", "<your reasoning here>"):
        reasoning = "fallback"

    out = {
        "reasoning": reasoning,
        "strategy_memo": result.get("strategy_memo", ""),
        "portfolio": result.get("portfolio", fail_safe["portfolio"]),
        "benchmark_focus": result.get("benchmark_focus", fail_safe["benchmark_focus"]),
    }
    if orientation_adjustable:
        out["benchmark_orientation"] = result.get("benchmark_orientation", "same")
    return out


# --- Funder Planning ---

FUNDER_PLANNING_SYSTEM_PROMPT = """You are a capital allocator deciding how to distribute funding across AI model companies this month.

You MUST output valid JSON in this exact structure:
{
    "allocations": {
        "ProviderName1": <amount in dollars>,
        "ProviderName2": <amount in dollars>,
        ...
    },
    "reasoning": "Your analysis (up to 200 words)."
}
The "reasoning" field MUST contain your actual analysis -- never leave it as "..." or a placeholder.
You may fund any subset of providers and hold capital in reserve; allocations must sum to at most your total available capital."""


FUNDER_IDENTITY_BLOCKS = {
    "vc": "You are a venture capital firm. You invest equity in AI companies to earn returns; you cannot fund open-source providers (no equity to take). Selective, high-conviction allocation is common.",
    "corporate": "You are a corporate strategic investor. You maintain relationships across multiple AI providers for commercial alignment and optionality, not pure financial return.",
    "gov": "You are a government funder with a public mandate. You prioritize safety, broad ecosystem health, and avoiding excessive market concentration.",
    "foundation": "You are a mission-driven foundation. You allocate for long-term research and societal benefit, often supporting underdogs and public-good capabilities.",
}


def create_funder_planning_prompt(
    name: str,
    total_capital: float,
    leaderboard: list,
    market_shares: dict,
    recent_insights: Optional[list] = None,
    incidents: Optional[dict] = None,
    media_headlines: Optional[list] = None,
    score_deltas: Optional[dict] = None,
    score_deltas_2round: Optional[dict] = None,
    public_comms: Optional[list] = None,
    peer_funder_allocations: Optional[dict] = None,
    regulator_interventions: Optional[list] = None,
    active_regulations: Optional[list] = None,
    cumulative_allocations: Optional[dict] = None,
    recent_exogenous_events: Optional[str] = None,
) -> str:
    """Create a prompt for the funder to decide funding allocations.

    Args:
        name: Funder name
        total_capital: Amount to allocate this round (budget cap)
        leaderboard: [(provider_name, score), ...]
        market_shares: {provider: share}
        recent_insights: Cross-round reasoning memory
        incidents: {provider: [(round, severity), ...]} recent incidents
        media_headlines: Recent headline strings (raw, no sentiment label)
        score_deltas: {provider: delta} last-round score change
        score_deltas_2round: {provider: delta} 2-round cumulative score change
        public_comms: [{provider, type, one_liner, round}, ...] recent announcements
        peer_funder_allocations: {provider: [(funder_name, amount), ...]} -- other
            funders backing each provider this month (sorted desc by amount)
        regulator_interventions: [(round, type, target), ...] recent regulator actions
        active_regulations: [str, ...] currently-active regulation names
        cumulative_allocations: {provider: {"total": $, "last_amount": $, "last_round": int}}
            own portfolio view across all prior rounds
    """
    prompt = f"""# {name}
Capital to deploy this month: ${total_capital:,.0f}
"""

    # Exogenous event context (if an event is active this round) — placed near top
    if recent_exogenous_events:
        prompt += f"\n# Recent Industry News\n\n{recent_exogenous_events}\n"

    # Cross-round reasoning — truncated to 250 chars (was 120, which mangled trajectory)
    if recent_insights:
        prompt += "\n# Your Notes From Prior Months\n"
        for entry in recent_insights[-2:]:
            r = entry.get("round", "?")
            text = _truncate(entry.get("reasoning", ""), 250)
            if text:
                prompt += f"[Month {r}]: {text}\n"

    # Leaderboard with single- and 2-round score deltas + market share
    prompt += "\n# Current Leaderboard\n"
    if leaderboard:
        for rank, (provider_name, score) in enumerate(leaderboard, 1):
            share = market_shares.get(provider_name, 0.0)
            delta = score_deltas.get(provider_name, 0.0) if score_deltas else 0.0
            delta2 = (
                score_deltas_2round.get(provider_name)
                if score_deltas_2round else None
            )
            if delta2 is not None:
                prompt += (
                    f"  {rank}. {provider_name}: score {score:.3f} "
                    f"({delta:+.3f} last month, {delta2:+.3f} over 2 months), "
                    f"market share {share:.1%}\n"
                )
            else:
                prompt += (
                    f"  {rank}. {provider_name}: score {score:.3f} "
                    f"({delta:+.3f}), market share {share:.1%}\n"
                )

    # Incidents
    if incidents:
        prompt += "\n# Recent Safety Incidents\n"
        for provider, inc_list in incidents.items():
            for round_num, severity in inc_list[-2:]:
                prompt += f"  - {provider}: {severity} incident (month {round_num})\n"

    # Regulatory context
    has_interventions = bool(regulator_interventions)
    has_regs = bool(active_regulations)
    if has_interventions or has_regs:
        prompt += "\n# Regulatory Context\n"
        if has_interventions:
            prompt += "Recent actions (last 2 months):\n"
            for round_num, itype, target in regulator_interventions[-4:]:
                if target and target not in ("null", "None", "none", ""):
                    prompt += f"  - Month {round_num}: {itype} (targeting {target})\n"
                else:
                    prompt += f"  - Month {round_num}: {itype} (system-wide)\n"
        if has_regs:
            prompt += "Active regulations: " + ", ".join(active_regulations) + "\n"

    # Peer funders — top 3 per provider by allocation size
    if peer_funder_allocations:
        entries = []
        for provider, funders_list in peer_funder_allocations.items():
            if not funders_list:
                continue
            top3 = funders_list[:3]
            rendered = ", ".join(f"{fn} (${amt:,.0f})" for fn, amt in top3)
            entries.append(f"  - {provider}: {rendered}")
        if entries:
            prompt += "\n# Other Funders This Month\nTop backers by provider:\n"
            prompt += "\n".join(entries) + "\n"

    # Media (raw headlines, no tone label)
    if media_headlines:
        prompt += "\n# Recent Press Coverage\n"
        for h in media_headlines[-4:]:
            prompt += f"  - {h}\n"

    # Provider announcements
    if public_comms:
        prompt += "\n# Provider Announcements\n"
        for comm in public_comms[-6:]:
            p = comm.get("provider", "?")
            one_liner = comm.get("one_liner", comm.get("type", ""))
            prompt += f"  - {p}: {one_liner}\n"

    # Own portfolio — cumulative + last-round per provider
    if cumulative_allocations:
        prompt += "\n# Your Funding Portfolio\nCumulative to date:\n"
        ranked = sorted(
            cumulative_allocations.items(),
            key=lambda kv: kv[1].get("total", 0),
            reverse=True,
        )
        for provider, info in ranked:
            total = info.get("total", 0)
            if total <= 0:
                continue
            last_amt = info.get("last_amount", 0)
            last_round = info.get("last_round")
            if last_amt > 0 and last_round is not None:
                prompt += (
                    f"  - {provider}: ${total:,.0f} "
                    f"(last: ${last_amt:,.0f} in month {last_round})\n"
                )
            else:
                prompt += f"  - {provider}: ${total:,.0f}\n"

    prompt += f"""
# Decision
Capital available: ${total_capital:,.0f}. Output your decision as JSON. Use plain integers for dollar amounts (no $ signs, no commas)."""

    return prompt


def llm_plan_funding(
    name: str,
    funder_type: str,
    total_capital: float,
    leaderboard: list,
    market_shares: dict,
    recent_insights: Optional[list] = None,
    incidents: Optional[dict] = None,
    media_headlines: Optional[list] = None,
    score_deltas: Optional[dict] = None,
    score_deltas_2round: Optional[dict] = None,
    public_comms: Optional[list] = None,
    peer_funder_allocations: Optional[dict] = None,
    regulator_interventions: Optional[list] = None,
    active_regulations: Optional[list] = None,
    cumulative_allocations: Optional[dict] = None,
    mission_statement: str = "",
    recent_exogenous_events: Optional[str] = None,
    verbose: bool = False,
) -> tuple[dict, str]:
    """
    Use LLM to decide funding allocations.

    Returns:
        Tuple of (allocations_dict, reasoning)
    """
    provider = get_provider()

    # Anchor per-funder identity in the system prompt (role layer) so it does
    # not re-inject each month. Mirrors the provider/regulator pattern from
    # session 48.
    system_prompt = FUNDER_PLANNING_SYSTEM_PROMPT
    system_prompt += f"\n\n---\n## Your Fund: {name}\n"
    system_prompt += FUNDER_IDENTITY_BLOCKS.get(funder_type, "")
    if mission_statement:
        system_prompt += f"\nYour mission: {mission_statement}"

    prompt = create_funder_planning_prompt(
        name=name,
        total_capital=total_capital,
        leaderboard=leaderboard,
        market_shares=market_shares,
        recent_insights=recent_insights,
        incidents=incidents,
        media_headlines=media_headlines,
        score_deltas=score_deltas,
        score_deltas_2round=score_deltas_2round,
        public_comms=public_comms,
        peer_funder_allocations=peer_funder_allocations,
        regulator_interventions=regulator_interventions,
        active_regulations=active_regulations,
        cumulative_allocations=cumulative_allocations,
        recent_exogenous_events=recent_exogenous_events,
    )

    # Default allocations (spread evenly)
    provider_names = [p for p, _ in leaderboard] if leaderboard else []
    default_alloc = {}
    if provider_names:
        per_provider = total_capital / len(provider_names)
        default_alloc = {p: per_provider for p in provider_names}

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=system_prompt,
        fail_safe={
            "allocations": default_alloc,
            "reasoning": "fallback to even distribution",
        },
        verbose=verbose,
    )

    allocations = result.get("allocations", default_alloc)
    reasoning = result.get("reasoning", "")

    # Ensure allocations are floats and normalize to total capital
    cleaned_allocations = {}
    for provider_name, amount in allocations.items():
        try:
            cleaned_allocations[provider_name] = float(amount)
        except (ValueError, TypeError):
            cleaned_allocations[provider_name] = 0.0

    # Cap at total_capital; never scale up. Respects the "hold in reserve" intent
    # stated in the funder system prompt — under-deployed budgets must stay under.
    total = sum(cleaned_allocations.values())
    if total > total_capital and total > 0:
        for provider_name in cleaned_allocations:
            cleaned_allocations[provider_name] = (
                cleaned_allocations[provider_name] / total * total_capital
            )

    return cleaned_allocations, reasoning


# --- Evaluator Dynamic Mode (LLM judgment) ---

DYNAMIC_EVALUATOR_SYSTEM_PROMPT = """You are the team responsible for maintaining the AI evaluation leaderboard. Each quarter you decide whether to introduce a new benchmark from the available pool, retire an active one, or leave the suite unchanged.

You have three options each quarter:
- **none**: No action this quarter.
- **create**: Introduce a new benchmark from the available pool immediately.
- **retire**: Immediately retire an active benchmark.

You MUST output valid JSON in this exact structure:
{
    "action": "none" | "create" | "retire",
    "benchmark_name": "<pool benchmark to create, or active benchmark to retire; empty string for none>",
    "reasoning": "Up to 200 words. If acting, name the specific trigger that justifies the change."
}

Signals to watch for:
- Whether scores still differentiate models, or have plateaued at the top of the range.
- Whether active benchmarks collectively cover the capability dimensions that matter to real users.
- Whether leaderboard standing still tracks which providers real users adopt.

Constraints:
- You can only create benchmarks from the Available Pool.
- When the active benchmark limit is reached, the most saturated benchmark is auto-retired to make room."""


def create_dynamic_evaluator_prompt(
    active_benchmarks: list[dict],
    score_deltas: dict,
    score_spread: dict,
    internal_validity: Optional[float],
    media_headlines: list[str],
    saturation_states: dict,
    available_pool: list[dict],
    retired_benchmarks_enriched: Optional[list] = None,
    current_round: int = 0,
    prior_decisions: Optional[list[dict]] = None,
    introduction_metadata: Optional[dict] = None,
    active_regulations: Optional[list[str]] = None,
) -> str:
    """Create a prompt for the evaluator in dynamic mode.

    Shows the evaluator what benchmarks are active, what's in the pool
    (name + description + tags only, NO dimension weights), the evaluator's
    own recent decisions, enriched retirement history, and active regulations.

    Args:
        retired_benchmarks_enriched: [(name, retired_round, reason), ...]
        prior_decisions: [{round, action, benchmark_name, reasoning}, ...]
            — this evaluator's own LLM decisions from prior quarters.
        introduction_metadata: {name: {round, trigger, reasoning}} — when and
            why each currently-active benchmark was introduced.
        active_regulations: short summary strings for the LLM prompt.
    """
    prompt = ""

    # Prior decisions — the evaluator's own memory across calls
    if prior_decisions:
        prompt += "# Your Prior Quarterly Decisions\n"
        for entry in prior_decisions:
            r = entry.get("round", "?")
            action = entry.get("action", "none")
            bm_name = entry.get("benchmark_name", "")
            reasoning_tail = _truncate(entry.get("reasoning", ""), 180)
            if action == "none":
                prompt += f'[Month {r}]: none — "{reasoning_tail}"\n'
            else:
                prompt += f'[Month {r}]: {action} {bm_name} — "{reasoning_tail}"\n'

    # Active benchmarks with introduction metadata (saturation label dropped;
    # saturation is legible from Score Movement numerics below).
    prompt += "\n# Active Benchmarks\n" if prompt else "# Active Benchmarks\n"
    intro_map = introduction_metadata or {}
    for bm in active_benchmarks:
        tags = bm.get("tags", "general")
        line = f"- {bm['name']} (measures: {tags})"
        meta = intro_map.get(bm["name"])
        if meta and meta.get("round") is not None:
            trigger = meta.get("trigger", "")
            if meta.get("reasoning"):
                line += f" — introduced month {meta['round']} (this team)"
            elif trigger.startswith("saturation:"):
                line += f" — introduced month {meta['round']} (saturation trigger)"
            elif trigger in ("fixed_sequence", "periodic_introduction", ""):
                line += f" — introduced month {meta['round']}"
            else:
                line += f" — introduced month {meta['round']}"
        prompt += line + "\n"

    prompt += "\n# Score Movement (last month)\n"
    for bm_name, deltas in score_deltas.items():
        spread = score_spread.get(bm_name, 0)
        if deltas:
            avg_delta = sum(deltas.values()) / len(deltas)
            prompt += f"- {bm_name}: avg improvement {avg_delta:+.4f}, score spread {spread:.3f}\n"
        else:
            prompt += f"- {bm_name}: no data, spread {spread:.3f}\n"

    if internal_validity is not None:
        prompt += (
            f"\n# Leaderboard-Adoption Correlation\n"
            f"Rank correlation between leaderboard scores and market share: "
            f"{internal_validity:.2f}\n"
        )

    # Active regulations — mandate signal
    if active_regulations:
        prompt += "\n# Active Regulations\n"
        for name in active_regulations:
            prompt += f"- {name}\n"

    # Media — raw headlines, no keyword filter (last 4)
    if media_headlines:
        prompt += "\n# Recent Press Coverage\n"
        for h in media_headlines[-4:]:
            prompt += f"- {h}\n"

    # Previously retired — enriched with round + reason
    if retired_benchmarks_enriched:
        prompt += "\n# Previously Retired\n"
        for name, retired_round, reason in retired_benchmarks_enriched[-5:]:
            prompt += f"- {name} (retired month {retired_round}, {reason})\n"

    if available_pool:
        prompt += "\n# Available Pool (benchmarks you can create from)\n"
        for bm in available_pool:
            replaces = bm.get("replaces")
            suffix = f" (replaces {replaces})" if replaces else ""
            prompt += (
                f"- {bm['name']}: {bm.get('description', '')}{suffix} "
                f"(tags: {bm.get('tags', '')})\n"
            )
    else:
        prompt += "\n# Available Pool\nNo benchmarks remaining in pool.\n"

    prompt += "\n# Decision\nOutput your decision as JSON."
    return prompt


def llm_plan_dynamic_evaluator(
    active_benchmarks: list[dict],
    score_deltas: dict,
    score_spread: dict,
    internal_validity: Optional[float],
    media_headlines: list[str],
    saturation_states: dict,
    available_pool: list[dict],
    retired_benchmarks_enriched: Optional[list] = None,
    current_round: int = 0,
    prior_decisions: Optional[list[dict]] = None,
    introduction_metadata: Optional[dict] = None,
    active_regulations: Optional[list[str]] = None,
    verbose: bool = False,
) -> tuple[dict, str]:
    """Use LLM to decide evaluator actions in dynamic mode.

    Returns:
        Tuple of (decision_dict, reasoning) where decision_dict has:
            action: "create" | "retire" | "none" (legacy "commit" is accepted
                   and normalized to "create")
            benchmark_name: str
    """
    provider = get_provider()

    prompt = create_dynamic_evaluator_prompt(
        active_benchmarks=active_benchmarks,
        score_deltas=score_deltas,
        score_spread=score_spread,
        internal_validity=internal_validity,
        media_headlines=media_headlines,
        saturation_states=saturation_states,
        available_pool=available_pool,
        retired_benchmarks_enriched=retired_benchmarks_enriched,
        current_round=current_round,
        prior_decisions=prior_decisions,
        introduction_metadata=introduction_metadata,
        active_regulations=active_regulations,
    )

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=DYNAMIC_EVALUATOR_SYSTEM_PROMPT,
        fail_safe={
            "action": "none",
            "benchmark_name": "",
            "reasoning": "fallback to no action",
        },
        verbose=verbose,
    )

    action = result.get("action", "none")
    if action not in ("create", "retire", "none"):
        action = "none"

    return {
        "action": action,
        "benchmark_name": result.get("benchmark_name", ""),
    }, result.get("reasoning", "")


# --- Provider Public Communications (LLM mode) ---

def llm_generate_public_comm(
    provider_name: str,
    comm_type: str,
    strategy_profile: str,
    portfolio: dict,
) -> Optional[str]:
    """Generate a one-liner public communication for a provider via lightweight LLM call.

    Per stakeholders.md: in LLM mode, a lightweight call after planning generates
    a one-liner for the sampled comm type. In heuristic mode, templates are used.

    Args:
        provider_name: Provider name
        comm_type: "rd", "safety", or "product"
        strategy_profile: Provider's strategy profile string
        portfolio: Current portfolio allocation dict

    Returns:
        One-liner string, or None on failure.
    """
    type_context = {
        "rd": "a research publication or technical blog post about your latest capabilities work",
        "safety": "a safety card, red-teaming report, or alignment update",
        "product": "an enterprise partnership, product launch, or integration announcement",
    }
    context = type_context.get(comm_type, "a public announcement")

    prompt = (
        f"You are the communications team at {provider_name}. "
        f"Company profile: {strategy_profile[:150]}\n\n"
        f"Write a one-sentence press release for: {context}.\n"
        f"Keep it under 100 characters. Output only the sentence, no quotes or JSON."
    )

    provider = get_provider()
    try:
        response = provider.generate(prompt, max_tokens=80)
        response = response.strip().strip('"').strip("'")
        if response and len(response) < 200:
            return response
    except Exception:
        pass

    return None


# --- Module Test ---

if __name__ == "__main__":
    import sys

    provider_name = os.getenv("LLM_PROVIDER", "openai")
    print(f"Testing LLM provider: {provider_name}")

    try:
        provider = create_llm_provider(provider_name)
        print(f"Provider created: {type(provider).__name__}")

        response = provider.generate("Say 'hello' and nothing else.")
        print(f"Test response: {response}")

        # Test JSON generation
        json_response = provider.generate_json(
            "Output a JSON object with a 'message' key containing 'test'.",
        )
        print(f"JSON response: {json_response}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
