"""Measure latency and throughput of the dependency-light inference path."""

from __future__ import annotations

import argparse
import statistics
import time

from aura_sqli import DetectionEngine


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1000)
    args = parser.parse_args()
    engine = DetectionEngine()
    samples = [
        "SELECT * FROM users WHERE id = 1",
        "SELECT * FROM users WHERE id = 1 OR 1=1 --",
        "UNION SELECT username,password FROM users",
        "SELECT * FROM orders WHERE customer_id = 44 ORDER BY created_at",
    ]
    latencies = []
    started = time.perf_counter()
    for i in range(args.iterations):
        t0 = time.perf_counter()
        engine.detect(samples[i % len(samples)])
        latencies.append((time.perf_counter() - t0) * 1000)
    elapsed = time.perf_counter() - started
    print(
        {
            "iterations": args.iterations,
            "throughput_qps": round(args.iterations / elapsed, 2),
            "latency_ms_avg": round(statistics.mean(latencies), 4),
            "latency_ms_p95": round(statistics.quantiles(latencies, n=20)[18], 4),
        }
    )


if __name__ == "__main__":
    main()

