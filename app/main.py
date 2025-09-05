from fastapi import FastAPI
from app.api.v1 import health
from app.core.config import settings
from app.core.logging import logger

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting...")
    yield
    print("Application shutting down...")

app = FastAPI(title=settings.app_name, lifespan=lifespan)

# routes
app.include_router(health.router, prefix="/api/v1", tags=["health"])
