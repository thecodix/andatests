"""Shared pytest fixtures for the backend test suite.

Points the app at a single temporary SQLite file for the whole test session
(never the real `backend/andatest.db` used for local development), imported
exactly once so every router/module shares the same `engine` instance —
reloading modules per-test caused stale engine references in some of them.
Each test gets a clean schema via create_all/drop_all around it.
"""
import os
import sys
import tempfile

import pytest

# Make top-level backend modules (config, database, main, models, auth, ...)
# importable, same convention as alembic/env.py and seed.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Must happen before any app module is imported anywhere in the test session.
_fd, _DB_PATH = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_DB_PATH}"

from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import SQLModel  # noqa: E402

import main as main_module  # noqa: E402
from database import engine  # noqa: E402
from rate_limit import limiter  # noqa: E402


@pytest.fixture()
def client():
    SQLModel.metadata.create_all(engine)
    with TestClient(main_module.app) as test_client:
        yield test_client
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    # Los contadores del limiter viven en memoria del propio proceso, fuera
    # del ciclo create_all/drop_all de cada test. Sin este reset, un test que
    # agote un límite (p.ej. el propio test de rate limiting) contaminaría
    # los tests siguientes que reutilizan el mismo endpoint.
    limiter.reset()
    yield
    limiter.reset()


def pytest_sessionfinish(session, exitstatus):
    engine.dispose()
    if os.path.exists(_DB_PATH):
        os.remove(_DB_PATH)
