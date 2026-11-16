"""Layer 2: semantic and lexical feature extraction."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from .normalization import NormalizedQuery


SQL_KEYWORDS = {
    "select", "insert", "update", "delete", "drop", "alter", "create", "from",
    "where", "and", "or", "union", "join", "having", "group", "order", "by",
    "sleep", "benchmark", "information_schema", "load_file", "outfile", "exec",
}
SUSPICIOUS_TOKENS = {
    "union", "sleep", "benchmark", "information_schema", "load_file", "outfile",
    "xp_cmdshell", "waitfor", "delay", "concat", "char", "cast", "declare",
}
OPERATORS = {"=", "<", ">", "<=", ">=", "!=", "<>", "or", "and", "&&", "||", "like"}
SPECIAL_CHARS = set("'\";#-%*/()=<>")
SIGNATURE_PATTERNS = {
    "tautology": re.compile(r"\b(or|and)\b\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?"),
    "union_select": re.compile(r"\bunion\b\s+(all\s+)?\bselect\b"),
    "stacked_query": re.compile(r";\s*(select|insert|update|delete|drop|alter|create)\b"),
    "comment_truncation": re.compile(r"(--|#|/\*)"),
    "time_based": re.compile(r"\b(sleep|benchmark|waitfor|delay)\b"),
    "metadata_probe": re.compile(r"\binformation_schema\b|sysobjects|sqlite_master"),
}


@dataclass(frozen=True)
class FeatureVector:
    values: dict[str, float]

    def to_ordered_list(self, names: list[str]) -> list[float]:
        return [self.values.get(name, 0.0) for name in names]


class SemanticFeatureExtractor:
    def extract(self, normalized: NormalizedQuery) -> FeatureVector:
        text = normalized.canonical
        tokens = normalized.tokens
        counts = Counter(tokens)
        length = max(len(text), 1)
        token_count = max(len(tokens), 1)

        features: dict[str, float] = {
            "query_length": float(len(text)),
            "token_count": float(len(tokens)),
            "token_diversity": len(set(tokens)) / token_count,
            "query_entropy": self._entropy(text),
            "special_char_density": sum(1 for c in text if c in SPECIAL_CHARS) / length,
            "sql_keyword_count": float(sum(counts[k] for k in SQL_KEYWORDS)),
            "sql_keyword_ratio": sum(counts[k] for k in SQL_KEYWORDS) / token_count,
            "operator_count": float(sum(counts[o] for o in OPERATORS)),
            "suspicious_token_count": float(sum(counts[t] for t in SUSPICIOUS_TOKENS)),
            "quote_count": float(text.count("'") + text.count('"')),
            "comment_removed": float(normalized.removed_comments),
            "url_decode_layers": float(normalized.decoded_layers),
        }
        for name, pattern in SIGNATURE_PATTERNS.items():
            features[f"sig_{name}"] = 1.0 if pattern.search(text) else 0.0
        features["signature_count"] = sum(features[f"sig_{name}"] for name in SIGNATURE_PATTERNS)
        return FeatureVector(features)

    @staticmethod
    def _entropy(text: str) -> float:
        if not text:
            return 0.0
        counts = Counter(text)
        total = len(text)
        return -sum((n / total) * math.log2(n / total) for n in counts.values())

