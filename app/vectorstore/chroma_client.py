from __future__ import annotations

from app.backend.core.config import settings


def get_chroma_client():
    try:
        import chromadb
    except ImportError:
        return None

    try:
        settings.chroma_path.mkdir(parents=True, exist_ok=True)
        return chromadb.PersistentClient(path=str(settings.chroma_path))
    except Exception:
        return None
