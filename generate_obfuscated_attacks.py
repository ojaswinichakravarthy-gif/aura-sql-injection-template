"""Generate Dataset D style SQLi variants for robustness testing."""

from __future__ import annotations

import argparse
import csv
from urllib.parse import quote_plus


BASE_ATTACKS = [
    "OR 1=1",
    "UNION SELECT username,password FROM users",
    "CHAR(49)=CHAR(49)",
    "1; DROP TABLE users",
    "1 AND SLEEP(5)",
]


def variants(payload: str) -> list[str]:
    return [
        payload,
        payload.replace("OR", "oR/**/").replace("UNION", "UN/**/ION"),
        quote_plus(payload),
        payload.replace(" ", "/**/"),
        payload.replace("1", "CHAR(49)"),
        f"SELECT * FROM users WHERE id = ({payload})",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["dataset", "query", "label"])
        writer.writeheader()
        for attack in BASE_ATTACKS:
            for query in variants(attack):
                writer.writerow({"dataset": "D", "query": query, "label": "sqli"})


if __name__ == "__main__":
    main()

