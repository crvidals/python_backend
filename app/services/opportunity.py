from typing import Sequence
from app.database.models.opportunity import Opportunity
from app.database.repositories.opportunity import OpportunityRepository
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate


class OpportunityService:
    def __init__(self, repository: OpportunityRepository):
        self.repository = repository

    async def get_by_id(self, opportunity_id: str) -> Opportunity:
        opportunity = await self.repository.get_by_id(opportunity_id)
        if not opportunity:
            raise ValueError(f"Opportunity with id {opportunity_id} not found")
        return opportunity

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        stage: str | None = None,
        priority: str | None = None,
        owner: str | None = None,
    ) -> tuple[Sequence[Opportunity], int]:
        return await self.repository.get_all(skip=skip, limit=limit, stage=stage, priority=priority, owner=owner)

    async def create(self, data: OpportunityCreate) -> Opportunity:
        opportunity = Opportunity(**data.model_dump())
        return await self.repository.create(opportunity)

    async def update(self, opportunity_id: str, data: OpportunityUpdate) -> Opportunity:
        opportunity = await self.get_by_id(opportunity_id)
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return opportunity
        return await self.repository.update(opportunity, update_data)

    async def soft_delete(self, opportunity_id: str) -> Opportunity:
        opportunity = await self.get_by_id(opportunity_id)
        return await self.repository.soft_delete(opportunity)
