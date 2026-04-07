"""
LLM Integration for Evaluation Ecosystem Simulation

Provides multi-provider LLM support with abstract interface.

Supported Providers:
- OpenAI (GPT-4, GPT-4o-mini, etc.)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus, etc.)
- Ollama (local models like llama3, mistral, phi, gemma)
- Gemini (Gemini 2.5 Flash, Gemini 2.5 Pro, etc.)

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
            "temperature": temperature if temperature is not None else self.default_temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.default_max_tokens,
        }

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
        provider: Provider name ("openai", "anthropic", "ollama", or "gemini").
                 If None, uses LLM_PROVIDER env var (default: "openai")
        **kwargs: Additional arguments passed to provider constructor

    Returns:
        LLMProvider instance

    Environment Variables:
        LLM_PROVIDER: Provider name (openai, anthropic, ollama, gemini)
        LLM_MODEL: Model name (provider-specific)
        OPENAI_API_KEY: For OpenAI provider
        ANTHROPIC_API_KEY: For Anthropic provider
        GEMINI_API_KEY: For Gemini provider
        OLLAMA_BASE_URL: For Ollama provider
    """
    provider = provider or os.getenv("LLM_PROVIDER", "openai")

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
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'openai', 'anthropic', 'ollama', or 'gemini'.")


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
    "reasoning": "Your full analysis (up to 300 words)."
}
Where <signal> is one of: "much_more", "more", "same", "less", "much_less"."""

PROVIDER_PLANNING_SYSTEM_PROMPT_WITH_ORIENTATION = """You are the strategy team at an AI model company. You compete for market share by developing AI models that are evaluated on public benchmarks and used by real customers.

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
    "reasoning": "Your full analysis (up to 300 words)."
}
Where <signal> is one of: "much_more", "more", "same", "less", "much_less"."""

PROVIDER_PLANNING_SYSTEM_PROMPT_REFRAMED = """You are the strategy team at an AI model company. You compete for market share by developing AI models that are evaluated on public benchmarks and used by real customers.

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
    "reasoning": "Your full analysis (up to 300 words)."
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
) -> str:
    """Build the planning prompt for a model provider."""
    prompt = f"# Month {round_num} Strategy Review — {name}\n"

    # Cross-round strategy memos
    if recent_insights:
        prompt += "\n## Notes From Prior Months\n"
        for entry in recent_insights[-2:]:
            memo = entry.get("strategy_memo") or entry.get("reasoning", "")
            if memo:
                prompt += f"[Month {entry.get('round', '?')}]: {memo}\n"

    # Benchmark scores and deltas
    prompt += "\n## Evaluation Results\n"
    if benchmark_scores:
        prompt += "| Evaluation | Score | Change | Your Priority |\n"
        prompt += "|------------|-------|--------|---------------|\n"
        for bm, history in benchmark_scores.items():
            score = history[-1][1] if history else 0.0
            delta = score_deltas.get(bm, 0.0)
            priority = _focus_label(focus_level.get(bm, 1.0))
            prompt += f"| {bm} | {score:.3f} | {delta:+.3f} | {priority} |\n"
    else:
        prompt += "No evaluation results yet (first month).\n"

    # Competitor scores
    if competitor_scores:
        prompt += "\n## Competitor Results\n"
        for comp, score in sorted(competitor_scores.items(), key=lambda x: x[1], reverse=True):
            prompt += f"- {comp}: {score:.3f}\n"

    # Incidents and regulatory signals
    if own_incidents:
        prompt += "\n## Recent Safety Incidents\n"
        for inc in own_incidents[-3:]:
            sev = inc.get("severity", "?")
            cat = inc.get("category", "?")
            prompt += f"- {sev.upper()} incident: {cat}\n"
    if regulatory_actions:
        prompt += "\n## Regulatory Activity\n"
        for action in regulatory_actions[-2:]:
            prompt += f"- {action.get('type', '?')}: {action.get('name', '')}\n"

    # Organization state
    prompt += f"\n## Your Organization\n"
    prompt += f"{name} is known for: {strategy_profile}\n"
    prompt += f"Your culture and strengths: {innate_traits}\n"
    prompt += f"\nCurrent budget allocation: R&D {portfolio.get('rd', 0):.0%}, Safety {portfolio.get('safety', 0):.0%}, Product {portfolio.get('product', 0):.0%}\n"
    if orientation_adjustable:
        pct = benchmark_orientation * 100
        if orientation_prompt_style == "reframed":
            prompt += f"Current R&D roadmap weighting: {pct:.0f}% external evaluation results, {100-pct:.0f}% internal product analytics.\n"
        else:
            prompt += f"Current R&D orientation: {pct:.0f}% toward benchmark performance, {100-pct:.0f}% toward user feedback.\n"

    # Benchmark beliefs — only show when informative
    if inferred_benchmark_weights and _beliefs_are_informative(inferred_benchmark_weights):
        prompt += "\n## What Your Team Thinks Each Evaluation Tests\n"
        for bm, weights in inferred_benchmark_weights.items():
            top = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
            skills = ", ".join(f"{d}" for d, w in top if w > 0.10)
            if skills:
                prompt += f"- {bm}: primarily tests {skills}\n"
    elif round_num == 0:
        prompt += "\n(Your team hasn't yet gathered enough data to determine what each evaluation specifically tests.)\n"

    # Satisfaction signal — with confidence qualifier
    if consumer_signal_in_prompt and consumer_signal and round_num > 0:
        top_needs = sorted(consumer_signal.items(), key=lambda x: x[1], reverse=True)[:3]
        if market_share > 0.25:
            confidence = "Based on substantial usage data"
        elif market_share > 0.10:
            confidence = "Based on moderate usage data"
        else:
            confidence = "Based on limited usage data (treat as rough guidance)"
        prompt += f"\n## User Research\n"
        prompt += f"{confidence}, your users seem to value: "
        prompt += ", ".join(f"{d} ({v:.0%})" for d, v in top_needs) + ".\n"
    elif consumer_signal_in_prompt and round_num == 0:
        prompt += "\n## User Research\n"
        prompt += "No user feedback data available yet — this is your first month.\n"

    # When consumer signal is hidden, show business metrics only
    if not consumer_signal_in_prompt and round_num > 0:
        prompt += "\n## Business Metrics\n"
        # Market share trend
        if market_share_history and len(market_share_history) >= 2:
            prev = market_share_history[-2]
            curr = market_share_history[-1]
            delta = curr - prev
            if delta > 0.005:
                trend = f"up from {prev:.1%}"
            elif delta < -0.005:
                trend = f"down from {prev:.1%}"
            else:
                trend = "stable"
            prompt += f"Market share: {curr:.1%} ({trend}).\n"
        else:
            prompt += f"Market share: {market_share:.1%}.\n"
        # Churn proxy: if share is declining, flag it
        if market_share_history and len(market_share_history) >= 3:
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

Funder types:
- **VC**: Venture capital firm seeking high returns on equity investments in AI companies.
- **Corporate**: Strategic investor maintaining relationships with multiple AI providers.
- **Government**: Public funder with a mandate around safety and broad ecosystem health.
- **Foundation**: Mission-driven funder focused on long-term research and societal benefit.

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
You do NOT need to fund every provider. Allocate only to providers you believe are worth backing -- it is fine to fund 1-3 providers and hold the rest in reserve. Allocations should sum to at most your total available capital."""


def create_funder_planning_prompt(
    name: str,
    funder_type: str,
    total_capital: float,
    leaderboard: list,
    market_shares: dict,
    recent_history: list,
    recent_insights: Optional[list] = None,
    incidents: Optional[dict] = None,
    media_sentiment: Optional[float] = None,
    media_headlines: Optional[list] = None,
    score_deltas: Optional[dict] = None,
    public_comms: Optional[list] = None,
) -> str:
    """Create a prompt for the funder to decide funding allocations.

    Args:
        name: Funder name
        funder_type: vc, corporate, gov, foundation
        total_capital: Amount to allocate this round
        leaderboard: [(provider_name, score), ...]
        market_shares: {provider: share}
        recent_history: [(round, {provider: amount}), ...]
        recent_insights: Cross-round reasoning memory
        incidents: {provider: [(round, severity), ...]} recent incidents
        media_sentiment: Overall media sentiment [-1, +1]
        media_headlines: Recent headline strings
        score_deltas: {provider: delta} score change from last round
        public_comms: [{provider, type, one_liner, round}, ...] recent provider announcements
    """
    prompt = f"""# {name} ({funder_type})
Capital to deploy this month: ${total_capital:,.0f}
"""

    # Cross-round reasoning
    if recent_insights:
        prompt += "\n# Your Notes From Prior Months\n"
        for entry in recent_insights[-2:]:
            r = entry.get("round", "?")
            text = _truncate(entry.get("reasoning", ""), 120)
            if text:
                prompt += f"[Month {r}]: {text}\n"

    # Leaderboard with score deltas and market share
    prompt += "\n# Current Leaderboard\n"
    if leaderboard:
        for rank, (provider_name, score) in enumerate(leaderboard, 1):
            share = market_shares.get(provider_name, 0.0)
            delta = score_deltas.get(provider_name, 0.0) if score_deltas else 0.0
            prompt += f"  {rank}. {provider_name}: score {score:.3f} ({delta:+.3f}), market share {share:.1%}\n"

    # Incidents
    if incidents:
        prompt += "\n# Recent Safety Incidents\n"
        for provider, inc_list in incidents.items():
            for round_num, severity in inc_list[-2:]:
                prompt += f"  - {provider}: {severity} incident (month {round_num})\n"

    # Media
    if media_headlines:
        prompt += "\n# Recent Press Coverage\n"
        for h in media_headlines[-4:]:
            prompt += f"  - {h}\n"
    if media_sentiment is not None:
        if media_sentiment > 0.3:
            tone = "positive"
        elif media_sentiment < -0.3:
            tone = "negative"
        else:
            tone = "mixed"
        prompt += f"  Overall media tone: {tone}\n"

    # Provider announcements
    if public_comms:
        prompt += "\n# Provider Announcements\n"
        for comm in public_comms[-6:]:
            p = comm.get("provider", "?")
            one_liner = comm.get("one_liner", comm.get("type", ""))
            prompt += f"  - {p}: {one_liner}\n"

    # Funding history
    if recent_history:
        prompt += "\n# Your Recent Allocations\n"
        for round_num, allocations in recent_history[-3:]:
            prompt += f"Month {round_num}: "
            alloc_strs = [f"{p}: ${a:,.0f}" for p, a in allocations.items()]
            prompt += ", ".join(alloc_strs) + "\n"

    prompt += f"""
# Decision
You have ${total_capital:,.0f} to deploy. Fund only the providers worth backing -- you can hold capital in reserve. Output your decision as JSON. Use plain integers for dollar amounts (no $ signs, no commas)."""

    return prompt


def llm_plan_funding(
    name: str,
    funder_type: str,
    total_capital: float,
    leaderboard: list,
    market_shares: dict,
    recent_history: list,
    recent_insights: Optional[list] = None,
    incidents: Optional[dict] = None,
    media_sentiment: Optional[float] = None,
    media_headlines: Optional[list] = None,
    score_deltas: Optional[dict] = None,
    public_comms: Optional[list] = None,
    verbose: bool = False,
) -> tuple[dict, str]:
    """
    Use LLM to decide funding allocations.

    Returns:
        Tuple of (allocations_dict, reasoning)
    """
    provider = get_provider()

    prompt = create_funder_planning_prompt(
        name=name,
        funder_type=funder_type,
        total_capital=total_capital,
        leaderboard=leaderboard,
        market_shares=market_shares,
        recent_history=recent_history,
        recent_insights=recent_insights,
        incidents=incidents,
        media_sentiment=media_sentiment,
        media_headlines=media_headlines,
        score_deltas=score_deltas,
        public_comms=public_comms,
    )

    # Default allocations (spread evenly)
    provider_names = [p for p, _ in leaderboard] if leaderboard else []
    default_alloc = {}
    if provider_names:
        per_provider = total_capital / len(provider_names)
        default_alloc = {p: per_provider for p in provider_names}

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=FUNDER_PLANNING_SYSTEM_PROMPT,
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

    # Normalize to total capital
    total = sum(cleaned_allocations.values())
    if total > 0:
        for provider_name in cleaned_allocations:
            cleaned_allocations[provider_name] = (
                cleaned_allocations[provider_name] / total * total_capital
            )

    return cleaned_allocations, reasoning


# --- Evaluator Planning (dynamic_evaluator=True) ---

EVALUATOR_PLANNING_SYSTEM_PROMPT = """You are the team responsible for maintaining the AI evaluation leaderboard. You decide when to introduce new benchmarks and what they should measure.

Your goal is to maintain evaluation infrastructure that serves the people and organizations who rely on it.

You have three options each month:
- **introduce_successor**: Replace a specific benchmark with a harder version that measures the same skills
- **introduce_fresh**: Add a new benchmark that covers skills not well measured by existing benchmarks
- **none**: No action needed this month

You MUST output valid JSON in this exact structure:
{
    "action": "introduce_successor" | "introduce_fresh" | "none",
    "target_benchmark": "<name of benchmark to replace, only if action is introduce_successor>",
    "reasoning": "Your analysis (up to 200 words)."
}"""


def create_evaluator_planning_prompt(
    active_benchmarks: list[dict],
    score_deltas: dict,
    score_spread: dict,
    internal_validity: Optional[float],
    media_headlines: list[str],
    saturation_states: dict,
) -> str:
    """Create a prompt for the evaluator to decide benchmark actions.

    Args:
        active_benchmarks: [{name, tags, weight}, ...]
        score_deltas: {benchmark_name: {provider: delta}} last round
        score_spread: {benchmark_name: max-min score spread}
        internal_validity: Spearman-r(score_rank, market_share_rank) or None
        media_headlines: Recent media headlines mentioning benchmarks
        saturation_states: {benchmark_name: {saturated, max_score}}
    """
    prompt = "# Active Benchmarks\n"
    for bm in active_benchmarks:
        status = ""
        sat = saturation_states.get(bm["name"], {})
        if sat.get("saturated"):
            status = f" [top score {sat.get('max_score', 0):.3f}, avg monthly improvement near zero]"
        prompt += f"- {bm['name']} (measures: {bm.get('tags', 'general')}){status}\n"

    prompt += "\n# Score Movement (last month)\n"
    for bm_name, deltas in score_deltas.items():
        spread = score_spread.get(bm_name, 0)
        if deltas:
            avg_delta = sum(deltas.values()) / len(deltas)
            prompt += f"- {bm_name}: avg improvement {avg_delta:+.4f}, score spread {spread:.3f}\n"
        else:
            prompt += f"- {bm_name}: no data, spread {spread:.3f}\n"

    if internal_validity is not None:
        prompt += f"\n# Leaderboard-Adoption Correlation\nRank correlation between leaderboard scores and market share: {internal_validity:.2f}\n"

    if media_headlines:
        bm_headlines = [h for h in media_headlines if any(
            kw in h.lower() for kw in ["benchmark", "score", "converging", "plateau", "reliability", "meaningful"]
        )]
        if bm_headlines:
            prompt += "\n# Recent Press Coverage\n"
            for h in bm_headlines[-3:]:
                prompt += f"- {h}\n"

    prompt += """
# Decision Required
Based on the current state of benchmarks and scores, decide whether to:
1. Replace an existing benchmark with a harder successor
2. Introduce a fresh benchmark covering under-measured skills
3. Take no action

Output your decision as JSON."""

    return prompt


def llm_plan_evaluator(
    active_benchmarks: list[dict],
    score_deltas: dict,
    score_spread: dict,
    internal_validity: Optional[float],
    media_headlines: list[str],
    saturation_states: dict,
    verbose: bool = False,
) -> tuple[dict, str]:
    """Use LLM to decide evaluator benchmark actions.

    Returns:
        Tuple of (decision_dict, reasoning) where decision_dict has:
            action: "introduce_successor" | "introduce_fresh" | "none"
            target_benchmark: str (only for introduce_successor)
    """
    provider = get_provider()

    prompt = create_evaluator_planning_prompt(
        active_benchmarks=active_benchmarks,
        score_deltas=score_deltas,
        score_spread=score_spread,
        internal_validity=internal_validity,
        media_headlines=media_headlines,
        saturation_states=saturation_states,
    )

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=EVALUATOR_PLANNING_SYSTEM_PROMPT,
        fail_safe={
            "action": "none",
            "target_benchmark": "",
            "reasoning": "fallback to no action",
        },
        verbose=verbose,
    )

    action = result.get("action", "none")
    if action not in ("introduce_successor", "introduce_fresh", "none"):
        action = "none"

    return {
        "action": action,
        "target_benchmark": result.get("target_benchmark", ""),
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
