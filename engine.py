"""End-to-end SQL injection detection engine."""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass

from .explainability import ExplanationEngine
from .feature_extractor import SemanticFeatureExtractor
from .modeling import HeuristicEnsemble, ModelPrediction
from .normalization import QueryNormalizer
from .structural_delta import StructuralDeltaAnalyzer
from .templates import AuraTemplateDB


@dataclass(frozen=True)
class DetectionResult:
    decision: str
    confidence: float
    threat_level: str
    normalized_query: str
    template: str
    model: str
    latency_ms: float
    reason: str
    influential_features: list[tuple[str, float]]
    component_scores: dict[str, float]

    def as_dict(self) -> dict:
        return asdict(self)


class DetectionEngine:
    def __init__(self, template_db: AuraTemplateDB | None = None) -> None:
        self.normalizer = QueryNormalizer()
        self.features = SemanticFeatureExtractor()
        self.structural = StructuralDeltaAnalyzer(template_db or AuraTemplateDB())
        self.model = HeuristicEnsemble()
        self.explainer = ExplanationEngine()

    def detect(self, query: str) -> DetectionResult:
        started = time.perf_counter()
        normalized = self.normalizer.normalize(query)
        semantic = self.features.extract(normalized).values
        structural_delta, template_match = self.structural.analyze(normalized)
        fused = {**semantic, **structural_delta.as_features()}
        prediction: ModelPrediction = self.model.predict(fused)
        explanation = self.explainer.explain(fused, prediction.score)
        latency = (time.perf_counter() - started) * 1000
        return DetectionResult(
            decision=prediction.label,
            confidence=round(prediction.score * 100, 3),
            threat_level=self._threat_level(prediction.score),
            normalized_query=normalized.canonical,
            template=template_match.template_name,
            model=prediction.model_name,
            latency_ms=round(latency, 3),
            reason=explanation.reason,
            influential_features=explanation.influential_features,
            component_scores=prediction.component_scores,
        )

    @staticmethod
    def _threat_level(score: float) -> str:
        if score >= 0.75:
            return "CRITICAL"
        if score >= 0.42:
            return "HIGH"
        if score >= 0.25:
            return "MEDIUM"
        return "LOW"
