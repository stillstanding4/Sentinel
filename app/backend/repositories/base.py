from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from app.models.database import session_scope


def model_to_dict(model: Any) -> dict[str, Any]:
    return {column.key: getattr(model, column.key) for column in inspect(model).mapper.column_attrs}


def models_to_dicts(models: list[Any]) -> list[dict[str, Any]]:
    return [model_to_dict(model) for model in models]


class BaseRepository:
    @contextmanager
    def session(self) -> Iterator[Session]:
        with session_scope() as db_session:
            yield db_session
