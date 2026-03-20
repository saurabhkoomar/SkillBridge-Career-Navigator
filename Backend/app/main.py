"""FastAPI entry point for Skill-Bridge Career Navigator API."""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import profile, analysis, roles, courses, data_route
from app.services.data_service import DataService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: load data; Shutdown: cleanup."""
    data_service = DataService()
    data_service.load_data()
    logger.info("Data loaded successfully")
    yield
    # Shutdown cleanup if needed
    pass


app = FastAPI(
    title="Skill-Bridge Career Navigator API",
    description="AI-powered career navigation platform that analyzes skills and creates personalized learning roadmaps",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router, prefix="/api")
app.include_router(analysis.router, prefix="/api")
app.include_router(roles.router, prefix="/api")
app.include_router(courses.router, prefix="/api")
app.include_router(data_route.router, prefix="/api")


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    ai_enabled = os.getenv("AI_ENABLED", "true").lower() == "true"
    return {
        "status": "healthy",
        "ai_enabled": ai_enabled,
        "ai_provider": "Groq (Llama 3)",
    }
