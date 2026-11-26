from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import Base, engine
from app.models import example  # noqa: F401 - registers models with SQLAlchemy
from app.routers import api, pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tables are created by Alembic migrations. This check keeps startup simple;
    # run `alembic upgrade head` before starting the application.
    yield


app = FastAPI(
    title="Hackathon Starter",
    description="Reusable FastAPI + PostgreSQL + SQLAlchemy + Jinja2 starter kit",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(pages.router)
app.include_router(api.router, prefix="/api")


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}
