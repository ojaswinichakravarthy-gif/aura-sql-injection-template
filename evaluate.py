"""Evaluate the framework on one or more unseen labeled datasets."""

from __future__ import annotations

import argparse
import json

from aura_sqli.evaluation import evaluate_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--datasets", nargs="+", required=True)
    args = parser.parse_args()
    report = {path: evaluate_csv(path) for path in args.datasets}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

