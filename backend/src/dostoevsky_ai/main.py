"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dostoevsky_ai.api.features.literary_rewrite import (
    router as literary_rewrite_router,
)
from dostoevsky_ai.api.features.inner_monologue import (
    router as inner_monologue_router,
)
from dostoevsky_ai.api.features.word_cabinet import (
    router as word_cabinet_router,
)
from dostoevsky_ai.api.health import router as health_router
from dostoevsky_ai.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Dostoevsky AI",
    description="Local literary writing and vocabulary assistant API.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.include_router(health_router, prefix="/api")
app.include_router(literary_rewrite_router, prefix="/api")
app.include_router(word_cabinet_router, prefix="/api")
app.include_router(inner_monologue_router, prefix="/api")
