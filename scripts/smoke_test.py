"""
Persistent smoke test for LLM provider billing verification.
Run before any bulk LLM sim to confirm provider routes calls through the expected billing source.

Usage:
    python smoke_test.py                 # default: claudecode provider, 1 call
    python smoke_test.py --provider anthropic
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from llm import create_llm_provider


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="claudecode",
                        choices=["claudecode", "anthropic", "openai", "ollama", "gemini"])
    parser.add_argument("--model", default="sonnet")
    args = parser.parse_args()

    print(f"[smoke] provider={args.provider} model={args.model}")
    print(f"[smoke] ANTHROPIC_API_KEY set in env: {bool(os.environ.get('ANTHROPIC_API_KEY'))}")

    provider = create_llm_provider(args.provider, model=args.model)
    print(f"[smoke] provider constructed: {type(provider).__name__}")

    t0 = time.time()
    result = provider.generate(
        prompt="Reply with exactly the word 'ok' and nothing else.",
        system_prompt="You are a smoke test. Respond minimally.",
        max_tokens=16,
    )
    dt = time.time() - t0

    print(f"[smoke] call completed in {dt:.2f}s")
    print(f"[smoke] response: {result!r}")
    print()
    print("[smoke] NOW CHECK YOUR BILLING CONSOLE:")
    print("  - Anthropic API console: https://console.anthropic.com/settings/usage")
    print("  - If usage ticked up for the API, claudecode is NOT using subscription billing.")
    print("  - If usage is unchanged, billing is routing through Claude Code subscription as expected.")


if __name__ == "__main__":
    main()
