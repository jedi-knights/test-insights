from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.adapters.inbound.http.routers import auth, health, projects, runs, suites, teams
from api.infrastructure.seed import provision_admin


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await provision_admin()
    yield


app = FastAPI(title="Test Insights API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(suites.router, prefix="/api/v1")
app.include_router(runs.router, prefix="/api/v1")
