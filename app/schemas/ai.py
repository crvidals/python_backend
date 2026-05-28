from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    conversation_id: str | None = None


class AIChatResponse(BaseModel):
    answer: str
    conversation_id: str
    sources: list[str] = []
