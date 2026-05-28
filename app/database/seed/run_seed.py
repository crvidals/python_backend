"""Seed script for initial data."""

import asyncio
import uuid
from datetime import date, datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import engine, async_session
from app.database.models.opportunity import Opportunity


async def seed_data():
    async with async_session() as session:
        result = await session.execute(
            text("SELECT COUNT(*) FROM opportunities")
        )
        count = result.scalar()
        if count > 0:
            print("Database already has data. Skipping seed.")
            return

        opportunities = [
            Opportunity(
                id=uuid.uuid4(),
                company_name="TechCorp Solutions",
                contact_name="María González",
                contact_email="maria.gonzalez@techcorp.com",
                opportunity_name="Implementación ERP TechCorp",
                description="Implementación completa de sistema ERP para gestión de inventarios y finanzas.",
                estimated_value=150000.0,
                currency="USD",
                stage="Propuesta enviada",
                priority="Alta",
                probability=65,
                owner="Carlos Pérez",
                next_follow_up_date=date(2026, 6, 15),
                last_interaction_summary="Se envió propuesta técnica y comercial. Esperando feedback del comité.",
                ai_recommendation="Priorizar seguimiento. Alta probabilidad de cierre si se responde antes del 15/06.",
                is_active=True,
            ),
            Opportunity(
                id=uuid.uuid4(),
                company_name="Global Retail Inc.",
                contact_name="Juan Martínez",
                contact_email="juan.martinez@globalretail.com",
                opportunity_name="Plataforma e-commerce Global Retail",
                description="Desarrollo de plataforma de comercio electrónico con integración a sistemas existentes.",
                estimated_value=85000.0,
                currency="USD",
                stage="Negociación",
                priority="Crítica",
                probability=80,
                owner="Ana López",
                next_follow_up_date=date(2026, 6, 5),
                last_interaction_summary="Reunión de negociación de términos. Cliente solicita descuento por volumen.",
                ai_recommendation="Ofrecer descuento del 5% por pago anticipado. Cierre probable esta semana.",
                is_active=True,
            ),
            Opportunity(
                id=uuid.uuid4(),
                company_name="Salud Digital S.A.",
                contact_name="Laura Fernández",
                contact_email="laura.fernandez@saluddigital.com",
                opportunity_name="App de telemedicina",
                description="Desarrollo de aplicación móvil para consultas médicas remotas con integración a historiales clínicos.",
                estimated_value=200000.0,
                currency="USD",
                stage="Diagnóstico",
                priority="Alta",
                probability=40,
                owner="Carlos Pérez",
                next_follow_up_date=date(2026, 6, 20),
                last_interaction_summary="Sesión de descubrimiento completada. Definición de requerimientos en proceso.",
                ai_recommendation="Programar demo de solución similar. Enfocar en seguridad y compliance HIPAA.",
                is_active=True,
            ),
            Opportunity(
                id=uuid.uuid4(),
                company_name="EduTech Academy",
                contact_name="Roberto Sánchez",
                contact_email="roberto.sanchez@edutech.com",
                opportunity_name="LMS personalizado EduTech",
                description="Plataforma de aprendizaje personalizado con IA para adaptación de contenidos.",
                estimated_value=120000.0,
                currency="USD",
                stage="Contactado",
                priority="Media",
                probability=25,
                owner="Ana López",
                next_follow_up_date=date(2026, 6, 10),
                last_interaction_summary="Primer contacto establecido. Interesados en agendar reunión de presentación.",
                ai_recommendation="Preparar caso de éxito de LMS similar. Enviar material corporativo.",
                is_active=True,
            ),
            Opportunity(
                id=uuid.uuid4(),
                company_name="LogiTrans Logistics",
                contact_name="Patricia Ruiz",
                contact_email="patricia.ruiz@logitrans.com",
                opportunity_name="Sistema de tracking LogiTrans",
                description="Sistema de rastreo y gestión de flotas en tiempo real con dashboard analítico.",
                estimated_value=95000.0,
                currency="USD",
                stage="Lead nuevo",
                priority="Baja",
                probability=10,
                owner="Carlos Pérez",
                next_follow_up_date=date(2026, 6, 25),
                last_interaction_summary="Lead ingresado desde formulario web. Pendiente primer contacto.",
                ai_recommendation="Contactar dentro de 48 horas. Ofrecer demo gratuita del producto.",
                is_active=True,
            ),
            Opportunity(
                id=uuid.uuid4(),
                company_name="FinanzaPro Consulting",
                contact_name="Diego Morales",
                contact_email="diego.morales@finanzapro.com",
                opportunity_name="Automatización reportes financieros",
                description="Automatización de generación de reportes financieros con IA y dashboards ejecutivos.",
                estimated_value=75000.0,
                currency="USD",
                stage="Ganado",
                priority="Media",
                probability=100,
                owner="Ana López",
                next_follow_up_date=None,
                last_interaction_summary="Contrato firmado. Inicio de proyecto programado para julio 2026.",
                ai_recommendation="Iniciar onboarding. Asignar equipo de implementación.",
                is_active=True,
            ),
        ]

        async with async_session() as seed_session:
            for opp in opportunities:
                seed_session.add(opp)
            await seed_session.commit()

        print(f"Seeded {len(opportunities)} opportunities successfully.")


if __name__ == "__main__":
    asyncio.run(seed_data())
