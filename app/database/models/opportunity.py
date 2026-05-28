import enum
from sqlalchemy import Column, String, Float, Integer, Date, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
import uuid
from app.database.models.base import Base


class StageEnum(str, enum.Enum):
    LEAD_NUEVO = "Lead nuevo"
    CONTACTADO = "Contactado"
    DIAGNOSTICO = "Diagnóstico"
    PROPUESTA_ENVIADA = "Propuesta enviada"
    NEGOCIACION = "Negociación"
    GANADO = "Ganado"
    PERDIDO = "Perdido"


class PriorityEnum(str, enum.Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    CRITICA = "Crítica"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=False)
    opportunity_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    estimated_value = Column(Float, nullable=True)
    currency = Column(String(10), default="USD")
    stage = Column(String(50), nullable=False, default=StageEnum.LEAD_NUEVO.value)
    priority = Column(String(50), nullable=False, default=PriorityEnum.MEDIA.value)
    probability = Column(Integer, nullable=False, default=0)
    owner = Column(String(255), nullable=True)
    next_follow_up_date = Column(Date, nullable=True)
    last_interaction_summary = Column(Text, nullable=True)
    ai_recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
