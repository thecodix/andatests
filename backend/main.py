from contextlib import asynccontextmanager
from pathlib import Path
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlmodel import SQLModel

from config import settings
from database import engine
from logging_config import configure_logging
from rate_limit import limiter
from routers import asistente, auth, notas, oposiciones, ranking, sesiones, stats, tarjetas, temas

configure_logging()
logger = logging.getLogger("andatest")

FRONTEND_DIR = Path(__file__).parent.parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Andatest API", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(temas.router, prefix="/api")
app.include_router(oposiciones.router, prefix="/api")
app.include_router(sesiones.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(ranking.router, prefix="/api")
app.include_router(asistente.router, prefix="/api")
app.include_router(notas.router, prefix="/api")
app.include_router(tarjetas.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Error no controlado en %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})


@app.get("/", include_in_schema=False)
def serve_index():
    # no-cache (not no-store): el navegador siempre revalida con el servidor
    # (If-None-Match/ETag) antes de usar la copia local, así que un deploy
    # nuevo se ve en el siguiente refresco en vez de quedar "pegado" con la
    # heurística de caché por defecto del navegador para FileResponse.
    return FileResponse(FRONTEND_DIR / "Tests Oposición.dc.html", headers={"Cache-Control": "no-cache"})


# Mounted last so API routes take precedence
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
