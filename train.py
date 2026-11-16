"""Train baseline SVM, RF, XGBoost, LightGBM, soft voting, weighted voting, and stacking candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.modeling import train_research_models


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", required=True)
    parser.add_argument("--model-dir", default="models/aura-hybrid-1.0.0")
    args = parser.parse_args()
    result = train_research_models(args.features, args.model_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

