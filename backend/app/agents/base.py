import json
import re

from anthropic import AsyncAnthropic

from app.config import ANTHROPIC_API_KEY, MODEL

client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)


async def ask_llm(system: str, user: str, max_tokens: int = 1200) -> str:
    response = await client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def parse_json(text: str) -> dict:
    """Pull a JSON object out of an LLM reply, tolerating code fences and stray prose."""
    cleaned = re.sub(r"```(?:json)?", "", text).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    try:
        return json.loads(match.group(0) if match else cleaned)
    except (json.JSONDecodeError, AttributeError):
        return {"raw": text}
