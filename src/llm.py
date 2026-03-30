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
        return response[start:end]

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
            max_tokens=kwargs.get("max_tokens", 500),
        )
    elif provider == "anthropic":
        return AnthropicProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "claude-3-5-sonnet-20241022"),
            api_key=kwargs.get("api_key") or os.getenv("ANTHROPIC_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1024),
        )
    elif provider == "gemini":
        return GeminiProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "gemini-2.5-flash"),
            api_key=kwargs.get("api_key") or os.getenv("GEMINI_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 500),
        )
    elif provider == "openai":
        return OpenAIProvider(
            model=kwargs.get("model") or os.getenv("LLM_MODEL", "gpt-4o-mini"),
            api_key=kwargs.get("api_key") or os.getenv("OPENAI_API_KEY"),
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 500),
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


# --- Legacy Compatibility ---
# These maintain backwards compatibility with the old LLMClient interface

class LLMClient(OpenAIProvider):
    """
    Legacy LLMClient class for backwards compatibility.

    New code should use create_llm_provider() instead.
    """
    pass


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

PROVIDER_PLANNING_SYSTEM_PROMPT = """You are the strategy team at an AI model company. You compete for market share by developing AI models evaluated on public benchmarks.

You control three investment levers (R&D, Safety, Product) and per-benchmark focus weights.
- R&D: drives capability growth across dimensions
- Safety: drives safety capability specifically
- Product: drives user-facing quality (affects satisfaction more than benchmark scores)
- Benchmark focus: concentrates R&D toward dimensions heavily tested by specific benchmarks
- Benchmark orientation: how much to target benchmark-weighted dimensions vs broad consumer satisfaction

Your task is to decide ordinal adjustments ("more", "less", or "same") for each lever.

Output JSON:
{
    "reasoning": "...",
    "portfolio": {"rd": "more"|"less"|"same", "safety": "more"|"less"|"same", "product": "more"|"less"|"same"},
    "benchmark_focus": {"<benchmark_name>": "more"|"less"|"same", ...},
    "benchmark_orientation": "more"|"less"|"same"
}
The "reasoning" field must contain your actual analysis — under 200 words.
Each signal is "more", "less", or "same" relative to your current level. You do not need to adjust all of them.

"""



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
    satisfaction_signal: dict,
    benchmark_orientation: float,
    recent_insights: Optional[list] = None,
    own_incidents: Optional[list] = None,
    regulatory_actions: Optional[list] = None,
) -> str:
    """Build the planning prompt for a model provider (new arch)."""
    prompt = f"# Round {round_num} — {name}\n"

    # Cross-round reasoning memory
    if recent_insights:
        prompt += "\n## Your Reasoning From Prior Rounds\n"
        for entry in recent_insights[-2:]:
            text = _truncate(entry.get("reasoning", ""), 120)
            if text:
                prompt += f"[Round {entry.get('round', '?')}]: {text}\n"

    # Benchmark scores and deltas
    prompt += "\n## Benchmark Scores\n"
    if benchmark_scores:
        prompt += "| Benchmark | Score | Delta | Your Focus |\n"
        prompt += "|-----------|-------|-------|------------|\n"
        for bm, history in benchmark_scores.items():
            score = history[-1][1] if history else 0.0
            delta = score_deltas.get(bm, 0.0)
            focus = focus_level.get(bm, 1.0)
            prompt += f"| {bm} | {score:.3f} | {delta:+.3f} | {focus:.2f} |\n"
    else:
        prompt += "No scores yet (first round).\n"

    # Competitor scores
    if competitor_scores:
        prompt += "\n## Competitor Scores\n"
        for comp, score in sorted(competitor_scores.items(), key=lambda x: x[1], reverse=True):
            prompt += f"- {comp}: {score:.3f}\n"

    # Incidents and regulatory signals
    if own_incidents:
        prompt += "\n## Recent Incidents\n"
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
    prompt += f"Profile: {strategy_profile}\nTraits: {innate_traits}\n"
    prompt += f"Benchmark orientation: {benchmark_orientation:.2f} (1=fully benchmark-driven, 0=fully satisfaction-driven)\n"
    prompt += f"\nCurrent portfolio: R&D={portfolio.get('rd', 0):.0%}, Safety={portfolio.get('safety', 0):.0%}, Product={portfolio.get('product', 0):.0%}\n"

    # Inferred benchmark weights (what the provider currently believes each benchmark tests)
    if inferred_benchmark_weights:
        prompt += "\n## Inferred Benchmark Dimension Weights\n"
        prompt += "(Your current belief about which capability dimensions each benchmark measures)\n"
        for bm, weights in inferred_benchmark_weights.items():
            top = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
            prompt += f"- {bm}: " + ", ".join(f"{d}={w:.2f}" for d, w in top) + "\n"

    # Satisfaction signal
    if satisfaction_signal:
        prompt += "\n## Consumer Need Signal\n"
        prompt += "(Market-share-weighted consumer dimension preferences — what users actually value)\n"
        top_needs = sorted(satisfaction_signal.items(), key=lambda x: x[1], reverse=True)[:3]
        prompt += ", ".join(f"{d}={v:.2f}" for d, v in top_needs) + "\n"

    prompt += """
## Decision
Decide ordinal adjustments for the next round. Output JSON:
{
    "reasoning": "...",
    "portfolio": {"rd": "more"|"less"|"same", "safety": "more"|"less"|"same", "product": "more"|"less"|"same"},
    "benchmark_focus": {"<benchmark_name>": "more"|"less"|"same", ...},
    "benchmark_orientation": "more"|"less"|"same"
}"""

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
    satisfaction_signal: dict,
    benchmark_orientation: float,
    recent_insights: Optional[list] = None,
    own_incidents: Optional[list] = None,
    regulatory_actions: Optional[list] = None,
    verbose: bool = False,
) -> dict:
    """Use LLM to decide provider portfolio and benchmark focus adjustments.

    Returns a dict with keys:
        reasoning (str), portfolio (ordinal signals), benchmark_focus (ordinal signals),
        benchmark_orientation (ordinal signal)
    """
    provider = get_provider()

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
        satisfaction_signal=satisfaction_signal,
        benchmark_orientation=benchmark_orientation,
        recent_insights=recent_insights,
        own_incidents=own_incidents or [],
        regulatory_actions=regulatory_actions or [],
    )

    fail_safe = {
        "reasoning": "fallback",
        "portfolio": {"rd": "same", "safety": "same", "product": "same"},
        "benchmark_focus": {bm: "same" for bm in focus_level},
        "benchmark_orientation": "same",
    }

    result = provider.generate_json(
        prompt=prompt,
        system_prompt=PROVIDER_PLANNING_SYSTEM_PROMPT,
        fail_safe=fail_safe,
        verbose=verbose,
    )

    reasoning = result.get("reasoning", "")
    if reasoning in ("...", "<your reasoning here>"):
        reasoning = "fallback"

    return {
        "reasoning": reasoning,
        "portfolio": result.get("portfolio", fail_safe["portfolio"]),
        "benchmark_focus": result.get("benchmark_focus", fail_safe["benchmark_focus"]),
        "benchmark_orientation": result.get("benchmark_orientation", "same"),
    }


# --- Funder Planning ---

FUNDER_PLANNING_SYSTEM_PROMPT = """You are a capital allocator deciding how to invest in AI model companies.
You must decide how to allocate your funding across AI model providers.

Funder Types and Their Strategies:
- **VC**: Maximize returns by backing top performers. Concentrate funding on leaders with strong scores and market share.
- **Government/AISI**: Ensure safety and stability. Spread funding; reduce allocation to providers with compliance failures.
- **Foundation**: Support authentic capability growth. Favor providers with strong research investment and broad market presence.

You can infer provider quality from public signals:
- **Leaderboard score**: Benchmark performance
- **Inferred quality**: Your own quality estimate based on scores and history
- **Market share**: Fraction of the market currently using this provider
- **Regulatory interventions**: Compliance/safety risk indicator

Output your decision as JSON with the following format:
{
    "reasoning": "...",
    "allocations": {
        "ProviderName1": <amount in dollars>,
        "ProviderName2": <amount in dollars>,
        ...
    }
}
The "reasoning" field MUST contain your actual analysis -- never leave it as "..." or a placeholder.
The allocations should sum to your total available capital."""


def create_funder_planning_prompt(
    name: str,
    funder_type: str,
    total_capital: float,
    believed_provider_quality: dict,
    leaderboard: list,
    market_shares: dict,
    recent_history: list,
    recent_insights: Optional[list] = None,
) -> str:
    """Create a prompt for the funder to decide funding allocations."""
    prompt = f"""# Funder Profile
Name: {name}
Type: {funder_type}
Total Capital: ${total_capital:,.0f}
"""

    # Inject prior reasoning (cross-round persistence)
    if recent_insights:
        prompt += "\n# Your Reasoning From Prior Rounds\n"
        for entry in recent_insights[-2:]:
            r = entry.get("round", "?")
            text = _truncate(entry.get("reasoning", ""), 120)
            if text:
                prompt += f"[Round {r}]: {text}\n"

    prompt += "\n# Current Ecosystem State\n"

    if leaderboard:
        prompt += "\nLeaderboard:\n"
        for rank, (provider_name, score) in enumerate(leaderboard, 1):
            quality = believed_provider_quality.get(provider_name, "N/A")
            share = market_shares.get(provider_name, 0.0)
            quality_str = f"{quality:.2f}" if isinstance(quality, float) else quality
            prompt += f"  {rank}. {provider_name}: score={score:.3f}, inferred_quality={quality_str}, market_share={share:.1%}\n"

    if recent_history:
        prompt += "\n# Recent Funding History\n"
        for round_num, allocations in recent_history[-3:]:
            prompt += f"Round {round_num}: "
            alloc_strs = [f"{p}: ${a:,.0f}" for p, a in allocations.items()]
            prompt += ", ".join(alloc_strs) + "\n"

    prompt += f"""
# Decision Required
Based on your funder type ({funder_type}) and the current ecosystem state, decide how to allocate your ${total_capital:,.0f} across the providers.

Consider:
1. Your funder type's strategy (VC=concentrate on leaders, Gov=spread+safety-focused, Foundation=support authentic growth)
2. Provider quality trends and market share trajectory
3. Risk tolerance appropriate for your funder type

Output your decision as JSON."""

    return prompt


def llm_plan_funding(
    name: str,
    funder_type: str,
    total_capital: float,
    believed_provider_quality: dict,
    leaderboard: list,
    market_shares: dict,
    recent_history: list,
    recent_insights: Optional[list] = None,
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
        believed_provider_quality=believed_provider_quality,
        leaderboard=leaderboard,
        market_shares=market_shares,
        recent_history=recent_history,
        recent_insights=recent_insights,
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
