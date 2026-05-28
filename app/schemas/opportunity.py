from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from uuid import UUID
from typing import Optional


class OpportunityBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    contact_name: str = Field(..., min_length=1, max_length=255)
    contact_email: str = Field(..., min_length=1, max_length=255)
    opportunity_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    estimated_value: Optional[float] = Field(None, ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=10)
    stage: str = Field(
        default="Lead nuevo",
        pattern=r"^(Lead nuevo|Contactado|Diagnóstico|Propuesta enviada|Negociación|Ganado|Perdido)$"
    )
    priority: str = Field(
        default="Media",
        pattern=r"^(Baja|Media|Alta|Crítica)$"
    )
    probability: int = Field(default=0, ge=0, le=100)
    owner: Optional[str] = Field(None, max_length=255)
    next_follow_up_date: Optional[date] = None
    last_interaction_summary: Optional[str] = None
    ai_recommendation: Optional[str] = None


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    contact_name: Optional[str] = Field(None, min_length=1, max_length=255)
    contact_email: Optional[str] = Field(None, min_length=1, max_length=255)
    opportunity_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    estimated_value: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=10)
    stage: Optional[str] = Field(
        None,
        pattern=r"^(Lead nuevo|Contactado|Diagnóstico|Propuesta enviada|Negociación|Ganado|Perdido)$"
    )
    priority: Optional[str] = Field(None, pattern=r"^(Baja|Media|Alta|Crítica)$")
    probability: Optional[int] = Field(None, ge=0, le=100)
    owner: Optional[str] = Field(None, max_length=255)
    next_follow_up_date: Optional[date] = None
    last_interaction_summary: Optional[str] = None
    ai_recommendation: Optional[str] = None


class OpportunityResponse(OpportunityBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class OpportunityListResponse(BaseModel):
    items: list[OpportunityResponse]
    total: int
    skip: int
    limit: int
