from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.repositories.opportunity import OpportunityRepository
from app.services.opportunity import OpportunityService
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityUpdate,
    OpportunityResponse,
    OpportunityListResponse,
)
from app.core.exceptions import NotFoundException

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


def get_opportunity_service(db: AsyncSession = Depends(get_db)) -> OpportunityService:
    repo = OpportunityRepository(db)
    return OpportunityService(repo)


@router.get("", response_model=OpportunityListResponse)
async def list_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    stage: str | None = None,
    priority: str | None = None,
    owner: str | None = None,
    service: OpportunityService = Depends(get_opportunity_service),
):
    items, total = await service.get_all(skip=skip, limit=limit, stage=stage, priority=priority, owner=owner)
    return OpportunityListResponse(
        items=[OpportunityResponse.model_validate(item) for item in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: str,
    service: OpportunityService = Depends(get_opportunity_service),
):
    opportunity = await service.get_by_id(opportunity_id)
    return OpportunityResponse.model_validate(opportunity)


@router.post("", response_model=OpportunityResponse, status_code=201)
async def create_opportunity(
    data: OpportunityCreate,
    service: OpportunityService = Depends(get_opportunity_service),
):
    opportunity = await service.create(data)
    return OpportunityResponse.model_validate(opportunity)


@router.put("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: str,
    data: OpportunityUpdate,
    service: OpportunityService = Depends(get_opportunity_service),
):
    opportunity = await service.update(opportunity_id, data)
    return OpportunityResponse.model_validate(opportunity)


@router.delete("/{opportunity_id}", status_code=204)
async def delete_opportunity(
    opportunity_id: str,
    service: OpportunityService = Depends(get_opportunity_service),
):
    await service.soft_delete(opportunity_id)
