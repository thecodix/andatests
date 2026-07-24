from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

from config import settings
from database import engine
from routers import asistente, auth, notas, ranking, sesiones, stats, temas

FRONTEND_DIR = Path(__file__).parent.parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Andatest API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(temas.router, prefix="/api")
app.include_router(sesiones.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(ranking.router, prefix="/api")
app.include_router(asistente.router, prefix="/api")
app.include_router(notas.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(FRONTEND_DIR / "Tests Oposición.dc.html")


# Mounted last so API routes take precedence
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
