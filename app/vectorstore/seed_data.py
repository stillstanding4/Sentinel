from __future__ import annotations

from app.demo.scenarios import POLICY_KNOWLEDGE_BASE as POLICY_DOCUMENTS
from app.vectorstore.chroma_client import get_chroma_client
from app.vectorstore.collections import POLICY_KNOWLEDGE_BASE


def seed_vectorstore() -> bool:
    client = get_chroma_client()
    if client is None:
        return False

    try:
        collection = client.get_or_create_collection(POLICY_KNOWLEDGE_BASE)
        embeddings = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        collection.upsert(
            ids=[f"policy_{index}" for index, _document in enumerate(POLICY_DOCUMENTS, start=1)],
            documents=POLICY_DOCUMENTS,
            metadatas=[{"source": "Demo Mode"} for _document in POLICY_DOCUMENTS],
            embeddings=embeddings[: len(POLICY_DOCUMENTS)],
        )
    except Exception:
        return False
    return True
