"""Layer 4: Structural delta analysis against Aura templates."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher

from .normalization import NormalizedQuery
from .templates import AuraTemplateDB, TemplateMatch


@dataclass(frozen=True)
class StructuralDelta:
    template_similarity: float
    template_mismatch: bool
    structural_delta: float
    extra_control_keywords: int
    predicate_complexity: int
    tautology_detected: bool
    stacked_query_detected: bool

    def as_features(self) -> dict[str, float]:
        return {
            "template_similarity": self.template_similarity,
            "template_mismatch": float(self.template_mismatch),
            "structural_delta": self.structural_delta,
            "extra_control_keywords": float(self.extra_control_keywords),
            "predicate_complexity": float(self.predicate_complexity),
            "tautology_detected": float(self.tautology_detected),
            "stacked_query_detected": float(self.stacked_query_detected),
        }


class StructuralDeltaAnalyzer:
    CONTROL = {"or", "and", "union", "select", "drop", "delete", "update", "insert", ";", "--"}

    def __init__(self, template_db: AuraTemplateDB | None = None) -> None:
        self.template_db = template_db or AuraTemplateDB()

    def analyze(self, normalized: NormalizedQuery) -> tuple[StructuralDelta, TemplateMatch]:
        match = self.template_db.match(normalized.canonical)
        tokens = normalized.tokens
        sequence_ratio = SequenceMatcher(None, tokens, match.expected_sequence).ratio()
        extra_control = max(0, sum(1 for t in tokens if t in self.CONTROL) - sum(1 for t in match.expected_sequence if t in self.CONTROL))
        predicate_complexity = tokens.count("or") + tokens.count("and") + tokens.count("=") + tokens.count("like")
        tautology = self._has_tautology(tokens)
        stacked = ";" in tokens
        delta = max(0.0, 1.0 - ((match.similarity + sequence_ratio) / 2.0))
        return (
            StructuralDelta(match.similarity, match.mismatch, delta, extra_control, predicate_complexity, tautology, stacked),
            match,
        )

    @staticmethod
    def _has_tautology(tokens: list[str]) -> bool:
        joined = " ".join(tokens)
        normalized = joined.replace("' ", "'").replace(" '", "'")
        return any(expr in normalized for expr in ["1 = 1", "'a' = 'a'", "\"a\" = \"a\"", "true = true"])

