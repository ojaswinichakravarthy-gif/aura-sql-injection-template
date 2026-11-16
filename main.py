"""FastAPI backend for real-time and batch SQLi detection."""

from __future__ import annotations

import logging
from typing import List

from pydantic import BaseModel

from aura_sqli import DetectionEngine

try:
    from fastapi import FastAPI
except Exception as exc:  # pragma: no cover
    raise RuntimeError("Install requirements.txt to run the FastAPI service.") from exc


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
app = FastAPI(title="Aura SQLi Detection API", version="1.0.0")
engine = DetectionEngine()


class QueryRequest(BaseModel):
    query: str


class BatchRequest(BaseModel):
    queries: List[str]


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": engine.model.name}


@app.post("/detect")
def detect(payload: QueryRequest) -> dict:
    result = engine.detect(payload.query).as_dict()
    logging.info("decision=%s confidence=%s latency_ms=%s", result["decision"], result["confidence"], result["latency_ms"])
    return result


@app.post("/detect/batch")
def detect_batch(payload: BatchRequest) -> dict:
    return {"results": [engine.detect(query).as_dict() for query in payload.queries]}

