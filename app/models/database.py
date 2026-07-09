from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.backend.core.config import settings


Base = declarative_base()


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@event.listens_for(Engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@contextmanager
def session_scope() -> Generator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def initialize_database() -> None:
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)

    # Import model modules before create_all so SQLAlchemy registers every PRD table.
    import app.models.agent  # noqa: F401
    import app.models.audit_run  # noqa: F401
    import app.models.feedback  # noqa: F401
    import app.models.hallucination_finding  # noqa: F401
    import app.models.policy_violation  # noqa: F401
    import app.models.recommendation  # noqa: F401
    import app.models.trust_score  # noqa: F401
    import app.models.user  # noqa: F401

    Base.metadata.create_all(bind=engine)
