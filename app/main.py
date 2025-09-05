from fastapi import FastAPI
from app.api.v1 import health, auth, social_accounts, orgs
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
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(social_accounts.router, prefix="/api/v1/social", tags=["Social Accounts"])
app.include_router(orgs.router, prefix="/api/v1/orgs", tags=["Organizations"])

