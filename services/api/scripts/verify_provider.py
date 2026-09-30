"""Connectivity check for the configured provider; never prints prompts or secrets."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.providers import MockProvider, ProviderError, configured_provider


def main():
    try:
        provider = configured_provider()
        result = provider.generate("pergunta técnica de teste", "contexto aprovado de teste")
        print(f"provider={provider.name} status=ok chars={len(result)}")
    except ProviderError as exc:
        print(f"provider=external status=unavailable reason={type(exc).__name__}")
        fallback = MockProvider().generate("teste", "contexto aprovado de teste")
        print(f"provider=mock-offline status=fallback-ok chars={len(fallback)}")


if __name__ == "__main__":
    main()
