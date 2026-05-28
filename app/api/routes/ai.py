from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.repositories.opportunity import OpportunityRepository
from app.services.opportunity import OpportunityService
from app.ai.services.chat import AIService
from app.schemas.ai import AIChatRequest, AIChatResponse

router = APIRouter(prefix="/ai", tags=["ai"])


def get_ai_service(db: AsyncSession = Depends(get_db)) -> AIService:
    repo = OpportunityRepository(db)
    opp_service = OpportunityService(repo)
    return AIService(opp_service)


@router.post("/chat", response_model=AIChatResponse)
async def ai_chat(
    request: AIChatRequest,
    ai_service: AIService = Depends(get_ai_service),
):
    return await ai_service.chat(request)
