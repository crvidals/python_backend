from typing import Any
from openai import AsyncOpenAI
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class OpenAIProvider:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        response = await self.client.chat.completions.create(**kwargs)
        return response.model_dump()
