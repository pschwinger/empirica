"""
Qdrant vector store for Empirica projects.
Collections per project:
- project_{project_id}_docs: documentation embeddings with metadata
- project_{project_id}_memory: findings/unknowns/mistakes/dead_ends embeddings
"""
from __future__ import annotations
import os
import json
from typing import Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue  # type: ignore
import requests

from .embeddings import get_embedding


def _get_qdrant_client() -> QdrantClient:
    url = os.getenv("EMPIRICA_QDRANT_URL")
    path = os.getenv("EMPIRICA_QDRANT_PATH", "./.qdrant_data")
    if url:
        return QdrantClient(url=url)
    return QdrantClient(path=path)


def _docs_collection(project_id: str) -> str:
    return f"project_{project_id}_docs"


def _memory_collection(project_id: str) -> str:
    return f"project_{project_id}_memory"


def init_collections(project_id: str) -> None:
    client = _get_qdrant_client()
    for name in (_docs_collection(project_id), _memory_collection(project_id)):
        if not client.collection_exists(name):
            client.create_collection(name, vectors_config=VectorParams(size=1536, distance=Distance.COSINE))


def upsert_docs(project_id: str, docs: List[Dict]) -> None:
    """
    docs: List of {id, text, metadata:{doc_path, tags, concepts, questions, use_cases}}
    """
    client = _get_qdrant_client()
    coll = _docs_collection(project_id)
    points: List[PointStruct] = []
    for d in docs:
        vector = get_embedding(d.get("text", ""))
        payload = {
            "doc_path": d.get("metadata", {}).get("doc_path"),
            "tags": d.get("metadata", {}).get("tags", []),
            "concepts": d.get("metadata", {}).get("concepts", []),
            "questions": d.get("metadata", {}).get("questions", []),
            "use_cases": d.get("metadata", {}).get("use_cases", []),
        }
        points.append(PointStruct(id=d["id"], vector=vector, payload=payload))
    if points:
        client.upsert(collection_name=coll, points=points)


def upsert_memory(project_id: str, items: List[Dict]) -> None:
    """
    items: List of {id, text, type: finding|unknown|mistake|dead_end}
    """
    client = _get_qdrant_client()
    coll = _memory_collection(project_id)
    points: List[PointStruct] = []
    for it in items:
        vector = get_embedding(it.get("text", ""))
        payload = {"type": it.get("type", "unknown")}
        points.append(PointStruct(id=it["id"], vector=vector, payload=payload))
    if points:
        client.upsert(collection_name=coll, points=points)


def _service_url() -> Optional[str]:
    return os.getenv("EMPIRICA_QDRANT_URL")


def _rest_search(collection: str, vector: List[float], limit: int) -> List[Dict]:
    url = _service_url()
    assert url, "EMPIRICA_QDRANT_URL must be set for REST search"
    resp = requests.post(
        f"{url}/collections/{collection}/points/search",
        json={"vector": vector, "limit": limit, "with_payload": True},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", [])


def search(project_id: str, query_text: str, kind: str = "all", limit: int = 5) -> Dict[str, List[Dict]]:
    client = _get_qdrant_client()
    qvec = get_embedding(query_text)
    results: Dict[str, List[Dict]] = {}

    # Prefer native search if available
    try:
        if hasattr(client, 'search') and callable(getattr(client, 'search')):
            if kind in ("all", "docs"):
                rd = client.search(collection_name=_docs_collection(project_id), query_vector=qvec, limit=limit, with_payload=True)
                results["docs"] = [
                    {
                        "score": getattr(r, 'score', 0.0) or 0.0,
                        "doc_path": (r.payload or {}).get("doc_path"),
                        "tags": (r.payload or {}).get("tags"),
                        "concepts": (r.payload or {}).get("concepts"),
                    }
                    for r in rd
                ]
            if kind in ("all", "memory"):
                rm = client.search(collection_name=_memory_collection(project_id), query_vector=qvec, limit=limit, with_payload=True)
                results["memory"] = [
                    {
                        "score": getattr(r, 'score', 0.0) or 0.0,
                        "type": (r.payload or {}).get("type"),
                    }
                    for r in rm
                ]
            return results
    except Exception:
        # Fall back to REST
        pass

    # REST fallback
    if kind in ("all", "docs"):
        rd = _rest_search(_docs_collection(project_id), qvec, limit)
        results["docs"] = [
            {
                "score": d.get('score', 0.0),
                "doc_path": (d.get('payload') or {}).get('doc_path'),
                "tags": (d.get('payload') or {}).get('tags'),
                "concepts": (d.get('payload') or {}).get('concepts'),
            }
            for d in rd
        ]
    if kind in ("all", "memory"):
        rm = _rest_search(_memory_collection(project_id), qvec, limit)
        results["memory"] = [
            {
                "score": m.get('score', 0.0),
                "type": (m.get('payload') or {}).get('type'),
            }
            for m in rm
        ]
    return results
