from langchain_anthropic import ChatAnthropic
import os


def get_llm():
    # Haiku 4.5 — modelo actual rápido/barato para loops de tool calling.
    # claude-3-haiku-20240307 fue retirado por Anthropic (devuelve 404).
    return ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        temperature=0.3,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=1024,
    )