"""Layer 6: local and global explanation helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Explanation:
    reason: str
    influential_features: list[tuple[str, float]]
    global_importance: list[tuple[str, float]]
    shap_available: bool = False


class ExplanationEngine:
    """Provides deterministic explanations and optional SHAP integration hooks."""

    DEFAULT_IMPORTANCE = {
        "structural_delta": 0.24,
        "template_mismatch": 0.18,
        "signature_count": 0.16,
        "suspicious_token_count": 0.12,
        "operator_count": 0.08,
        "query_entropy": 0.06,
        "special_char_density": 0.06,
        "url_decode_layers": 0.05,
        "comment_removed": 0.05,
    }

    def explain(self, features: dict[str, float], score: float) -> Explanation:
        ranked = sorted(
            ((name, value) for name, value in features.items() if abs(value) > 0),
            key=lambda item: abs(item[1]) * self.DEFAULT_IMPORTANCE.get(item[0], 0.03),
            reverse=True,
        )[:8]
        if score >= 0.75:
            reason = "Multiple structural and semantic SQL injection indicators were present."
        elif score >= 0.45:
            reason = "The query partially diverges from known legitimate templates and contains suspicious markers."
        else:
            reason = "The query is close to legitimate Aura templates and lacks strong injection indicators."
        return Explanation(reason, ranked, sorted(self.DEFAULT_IMPORTANCE.items(), key=lambda x: x[1], reverse=True))

