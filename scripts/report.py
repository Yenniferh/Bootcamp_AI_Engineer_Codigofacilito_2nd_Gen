"""Reporte de llamadas al LLM a partir de logs/llm_calls.jsonl.

Uso:
    uv run scripts/report.py [ruta/al/archivo.jsonl]
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

DEFAULT_PATH = Path("logs/llm_calls.jsonl")
GRAY = "\033[90m"
RESET = "\033[0m"


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    file_location = argv[0] if argv else None
    events = load_logs_file(file_location)
    if not events:
        return 1

    metrics = calculate_metrics_from_events(events)

    formatted_output = " · ".join(
        [f"{key.replace('_', ' ').title()}: {value}" for key, value in metrics.items()]
    )
    print(f"{GRAY}{formatted_output}{RESET}")
    return 0


def load_logs_file(logs_path: str | None):
    try:
        path = Path(logs_path) if logs_path else DEFAULT_PATH
        lines = path.read_text(encoding="utf-8").splitlines()
        events = [json.loads(line) for line in lines if line.strip()]
        if not events:
            raise ValueError("No events found in log file")
        return events
    except FileNotFoundError:
        print(f"Error: File not found at {path.name}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {path.name}")
    except ValueError as ve:
        print(f"Error: {ve} {path.name}")
    return None


def calculate_metrics_from_events(events):
    is_fallback = 0
    providers_calls = {}
    models_calls = {}
    total_cost = 0
    latency = []
    for event in events:
        provider = event["provider"]
        model = event["model"]
        providers_calls[provider] = providers_calls.get(provider, 0) + 1
        models_calls[model] = models_calls.get(model, 0) + 1
        is_fallback = is_fallback + 1 if bool(event["fallback"]) else is_fallback
        if event["success"]:
            latency.append(event["latency_ms"])
        total_cost += event["cost_usd"]

    q = statistics.quantiles(latency, n=100, method="inclusive") if len(latency) >= 2 else None
    # Python lists use zero-based indexing
    q_50 = q[49] if q else None
    q_95 = q[94] if q else None
    fallback_calls_rate = int(is_fallback / len(events) * 100)
    return {
        "calls": len(events),
        "fallback_calls_rate": fallback_calls_rate,
        "total_cost": round(total_cost, 6),
        "q_50": q_50,
        "q_95": q_95,
        "provider_calls": providers_calls,
        "models_calls": models_calls,
    }


if __name__ == "__main__":
    sys.exit(main())
