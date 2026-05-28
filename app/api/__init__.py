from fastapi import APIRouter
from app.api.routes import health, opportunities, ai

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(opportunities.router)
v1_router.include_router(ai.router)

api_router.include_router(v1_router)
