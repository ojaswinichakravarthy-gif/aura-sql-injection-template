"""Convert labeled SQL datasets into research feature matrices."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from aura_sqli.engine import DetectionEngine
from aura_sqli.modeling import FEATURE_ORDER


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    engine = DetectionEngine()
    rows = []
    for source in args.input:
        with Path(source).open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                norm = engine.normalizer.normalize(row["query"])
                semantic = engine.features.extract(norm).values
                structural, _ = engine.structural.analyze(norm)
                rows.append({"query": row["query"], "label": row["label"], **semantic, **structural.as_features()})

    with Path(args.output).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["query", "label", *FEATURE_ORDER])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()

