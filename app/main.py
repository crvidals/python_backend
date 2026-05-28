from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import get_settings
from app.core.exceptions import global_exception_handler
from app.api import api_router

settings = get_settings()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CRM AI Assistant API...")
    routes = [r.path for r in app.routes]
    logger.info(f"Registered routes: {routes}")
    logger.info("Swagger UI available at: /docs")
    logger.info("Redoc available at: /redoc")
    logger.info("API is ready to accept requests")
    yield
    logger.info("Shutting down CRM AI Assistant API...")


app = FastAPI(
    title="CRM AI Assistant API",
    description="Backend profesional para sistema CRM con asistente de IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)
app.include_router(api_router)

logger.info(f"FastAPI app created with {len(app.routes)} routes")
