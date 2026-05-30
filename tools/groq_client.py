"""Centralised Groq client — single instance shared across all agents."""
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
_client: Groq | None = None

def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not set. Get a free key at https://console.groq.com")
        _client = Groq(api_key=api_key)
    return _client

def chat(
    messages: list[dict],
    system: str = "",
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> str:
    client = get_client()
    full_messages = []
    if system:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)
    response = client.chat.completions.create(
        model=model, messages=full_messages,
        temperature=temperature, max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
