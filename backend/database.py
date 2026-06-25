from sqlalchemy import event
from sqlmodel import Session, create_engine

from config import settings

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.database_url, connect_args=connect_args, echo=False)


@event.listens_for(engine, "connect")
def _sqlite_pragmas(dbapi_conn, _):
    if settings.database_url.startswith("sqlite"):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")


def get_session():
    with Session(engine) as session:
        yield session
