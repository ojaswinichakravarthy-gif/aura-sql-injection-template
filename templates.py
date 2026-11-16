"""Layer 3: Aura template intelligence database."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
from pathlib import Path

from .normalization import QueryNormalizer


LITERAL_RE = re.compile(r"'[^']*'|\"[^\"]*\"|\b\d+(\.\d+)?\b")


@dataclass(frozen=True)
class AuraTemplate:
    name: str
    query_pattern: str
    query_tree: dict[str, list[str]]
    token_sequence: list[str]


@dataclass(frozen=True)
class TemplateMatch:
    template_name: str
    similarity: float
    mismatch: bool
    expected_sequence: list[str]


class AuraTemplateDB:
    def __init__(self, templates: list[AuraTemplate] | None = None) -> None:
        self.normalizer = QueryNormalizer()
        self.templates = self.default_templates() if templates is None else templates

    @classmethod
    def from_json(cls, path: str | Path) -> "AuraTemplateDB":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls([AuraTemplate(**item) for item in data["templates"]])

    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps({"templates": [asdict(t) for t in self.templates]}, indent=2),
            encoding="utf-8",
        )

    def match(self, canonical_query: str) -> TemplateMatch:
        structure = self.structure(canonical_query)
        best = max(
            self.templates,
            key=lambda t: SequenceMatcher(None, structure, t.query_pattern).ratio(),
        )
        score = SequenceMatcher(None, structure, best.query_pattern).ratio()
        return TemplateMatch(best.name, score, score < 0.72, best.token_sequence)

    def structure(self, query: str) -> str:
        normalized = self.normalizer.normalize(query).canonical
        normalized = LITERAL_RE.sub("?", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    @classmethod
    def build_template(cls, name: str, query: str) -> AuraTemplate:
        normalizer = QueryNormalizer()
        normalized = normalizer.normalize(query).canonical
        pattern = LITERAL_RE.sub("?", normalized)
        pattern = re.sub(r"\s+", " ", pattern).strip()
        tokens = normalizer.normalize(pattern).tokens
        return AuraTemplate(name, pattern, cls._tree(tokens), tokens)

    @staticmethod
    def _tree(tokens: list[str]) -> dict[str, list[str]]:
        clauses = {"select": [], "from": [], "where": [], "values": [], "other": []}
        current = "other"
        for token in tokens:
            if token in clauses:
                current = token
                continue
            clauses[current].append(token)
        return clauses

    @classmethod
    def default_templates(cls) -> list[AuraTemplate]:
        examples = {

            # Authentication
        "login_username":
            "SELECT * FROM users WHERE username = ?",

        "login_email":
            "SELECT * FROM users WHERE email = ?",

        "session_lookup":
            "SELECT * FROM sessions WHERE token = ?",

        # User Management
        "user_by_id":
            "SELECT * FROM users WHERE id = ?",

        "user_profile":
            "SELECT name,email,phone FROM users WHERE id = ?",

        "update_profile":
            "UPDATE users SET email = ? WHERE id = ?",

        "delete_session":
            "DELETE FROM sessions WHERE session_id = ?",

        # Products
        "product_by_id":
            "SELECT * FROM products WHERE product_id = ?",

        "product_search":
            "SELECT * FROM products WHERE category = ?",

        "product_reviews":
            "SELECT * FROM reviews WHERE product_id = ?",

        # Orders
        "order_by_id":
            "SELECT * FROM orders WHERE order_id = ?",

        "orders_by_customer":
            "SELECT * FROM orders WHERE customer_id = ?",

        "insert_order":
            "INSERT INTO orders VALUES (?, ?, ?)",

        # Shopping Cart
        "cart_lookup":
            "SELECT * FROM cart WHERE user_id = ?",

        "cart_update":
            "UPDATE cart SET quantity = ? WHERE user_id = ?",

        # Blog / CMS
        "article_by_slug":
            "SELECT * FROM articles WHERE slug = ?",

        "article_comments":
            "SELECT * FROM comments WHERE article_id = ?",

        # Feedback
        "insert_feedback":
            "INSERT INTO feedback VALUES (?, ?, ?)",

        # Search
        "search_title":
            "SELECT * FROM documents WHERE title LIKE ?",

        # Admin
        "admin_user_lookup":
            "SELECT * FROM users WHERE role = ?",

        # Password Reset
        "reset_token":
            "SELECT * FROM password_reset WHERE token = ?",

        # Notifications
        "notification_lookup":
            "SELECT * FROM notifications WHERE user_id = ?",

        # Audit Logs
        "audit_logs":
            "SELECT * FROM audit_logs WHERE user_id = ?",

        # Settings
        "user_settings":
            "SELECT * FROM settings WHERE user_id = ?",

        # Messages
        "message_lookup":
            "SELECT * FROM messages WHERE receiver_id = ?",

        # Wishlist
        "wishlist_lookup":
            "SELECT * FROM wishlist WHERE user_id = ?"

        }       
    
        return [
        cls.build_template(name, query) for name, query in examples.items()

        ]