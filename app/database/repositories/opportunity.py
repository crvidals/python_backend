from typing import Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.opportunity import Opportunity


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


class OpportunityRepository(BaseRepository):
    async def get_by_id(self, opportunity_id: str) -> Opportunity | None:
        result = await self.db_session.execute(
            select(Opportunity).where(
                Opportunity.id == opportunity_id,
                Opportunity.is_active == True
            )
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        stage: str | None = None,
        priority: str | None = None,
        owner: str | None = None,
    ) -> tuple[Sequence[Opportunity], int]:
        query = select(Opportunity).where(Opportunity.is_active == True)
        count_query = select(func.count()).select_from(Opportunity).where(Opportunity.is_active == True)

        if stage:
            query = query.where(Opportunity.stage == stage)
            count_query = count_query.where(Opportunity.stage == stage)
        if priority:
            query = query.where(Opportunity.priority == priority)
            count_query = count_query.where(Opportunity.priority == priority)
        if owner:
            query = query.where(Opportunity.owner == owner)
            count_query = count_query.where(Opportunity.owner == owner)

        count_result = await self.db_session.execute(count_query)
        total = count_result.scalar_one()

        query = query.offset(skip).limit(limit).order_by(Opportunity.created_at.desc())
        result = await self.db_session.execute(query)
        items = result.scalars().all()

        return items, total

    async def create(self, opportunity: Opportunity) -> Opportunity:
        self.db_session.add(opportunity)
        await self.db_session.flush()
        await self.db_session.refresh(opportunity)
        return opportunity

    async def update(self, opportunity: Opportunity, update_data: dict) -> Opportunity:
        for key, value in update_data.items():
            setattr(opportunity, key, value)
        await self.db_session.flush()
        await self.db_session.refresh(opportunity)
        return opportunity

    async def soft_delete(self, opportunity: Opportunity) -> Opportunity:
        opportunity.is_active = False
        await self.db_session.flush()
        await self.db_session.refresh(opportunity)
        return opportunity
