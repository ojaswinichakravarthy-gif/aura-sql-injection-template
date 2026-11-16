"""Layer 1: canonical SQL query normalization."""

from __future__ import annotations

import html
import re
import unicodedata
from dataclasses import dataclass
from urllib.parse import unquote_plus


SQL_COMMENT_RE = re.compile(r"(--[^\n\r]*|#[^\n\r]*|/\*.*?\*/)", re.DOTALL)
HEX_LITERAL_RE = re.compile(r"\b0x([0-9a-fA-F]{2,})\b")
CHAR_FUNC_RE = re.compile(r"\bchar\s*\(([\d,\s]+)\)", re.IGNORECASE)
TOKEN_RE = re.compile(
    r"[a-z_][a-z0-9_]*|\d+\.\d+|\d+|<=|>=|<>|!=|==|&&|\|\||[(),=*<>+\-/;%'.?]",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class NormalizedQuery:
    raw: str
    canonical: str
    tokens: list[str]
    removed_comments: int
    decoded_layers: int


class QueryNormalizer:
    """Converts raw input into a stable representation resistant to obfuscation."""

    def normalize(self, query: str) -> NormalizedQuery:
        if query is None:
            query = ""
        raw = str(query)
        decoded, layers = self._iterative_url_decode(raw)
        decoded = html.unescape(decoded)
        decoded = unicodedata.normalize("NFKC", decoded)
        decoded = self._decode_char_functions(decoded)
        decoded = self._decode_hex_literals(decoded)
        decoded = decoded.lower()
        without_comments, removed_comments = SQL_COMMENT_RE.subn(" ", decoded)
        cleaned = self._cleanup_obfuscation(without_comments)
        canonical = re.sub(r"\s+", " ", cleaned).strip()
        tokens = TOKEN_RE.findall(canonical)
        return NormalizedQuery(raw, canonical, tokens, removed_comments, layers)

    @staticmethod
    def _iterative_url_decode(value: str, max_rounds: int = 4) -> tuple[str, int]:
        current = value
        rounds = 0
        for _ in range(max_rounds):
            nxt = unquote_plus(current)
            if nxt == current:
                break
            current = nxt
            rounds += 1
        return current, rounds

    @staticmethod
    def _decode_hex_literals(value: str) -> str:
        def replace(match: re.Match[str]) -> str:
            payload = match.group(1)
            if len(payload) % 2:
                return match.group(0)
            try:
                decoded = bytes.fromhex(payload).decode("utf-8", errors="ignore")
            except ValueError:
                return match.group(0)
            return decoded if decoded.strip() else match.group(0)

        return HEX_LITERAL_RE.sub(replace, value)

    @staticmethod
    def _decode_char_functions(value: str) -> str:
        def replace(match: re.Match[str]) -> str:
            try:
                nums = [int(x.strip()) for x in match.group(1).split(",") if x.strip()]
                return "".join(chr(n) for n in nums if 0 <= n <= 255)
            except ValueError:
                return match.group(0)

        return CHAR_FUNC_RE.sub(replace, value)

    @staticmethod
    def _cleanup_obfuscation(value: str) -> str:
        # Recover common split-keyword obfuscation after comments are removed.
        value = re.sub(r"\b(o)\s+(r)\b", r"\1\2", value)
        value = re.sub(r"\b(un)\s+(ion)\b", r"\1\2", value)
        value = re.sub(r"\b(sel)\s+(ect)\b", r"\1\2", value)
        value = re.sub(r"\s*([=<>(),;+\-*/%])\s*", r" \1 ", value)
        return value

