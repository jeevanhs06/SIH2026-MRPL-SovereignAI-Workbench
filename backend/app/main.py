from fastapi import FastAPI

from app.config import get_settings
from app.routes import auth, documents, health, knowledge, security, tasks

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(knowledge.router)
app.include_router(tasks.router)
app.include_router(security.router)
