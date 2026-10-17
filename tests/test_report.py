from scripts.report import (
    calculate_metrics_from_events,
    load_logs_file,
)


def test_load_logs_file_not_found():
    filepath = "logs/not_found.jsonl"
    events = load_logs_file(filepath)
    assert events is None


def test_load_logs_file_reads_empty_file(tmp_path):
    filepath = tmp_path / "empty.jsonl"
    filepath.write_text("", encoding="utf-8")

    events = load_logs_file(str(filepath))

    assert events is None


def test_load_logs_file_reads_events(tmp_path):
    ALL_SUCCESS_EVENTS = """
    {"request_id": "aab80e50", "timestamp": "2026-10-11T01:57:47.700782+00:00", "provider": "gemini", "model": "gemini-3.5-flash-lite", "tokens_in": 76, "tokens_out": 72, "latency_ms": 1004.5, "ttft_ms": null, "cost_usd": 0.00020280000000000002, "fallback": false, "success": true, "error_type": null, "prompt_chars": 330}
    {"request_id": "73e5c691", "timestamp": "2026-10-12T20:44:01.634266+00:00", "provider": "groq", "model": "openai/gpt-oss-120b", "tokens_in": 105, "tokens_out": 45, "latency_ms": 678.1, "ttft_ms": null, "cost_usd": 4.275e-05, "fallback": false, "success": true, "error_type": null, "prompt_chars": 129}
    """  # noqa: E501
    filepath = tmp_path / "logs.jsonl"
    filepath.write_text(ALL_SUCCESS_EVENTS, encoding="utf-8")

    events = load_logs_file(str(filepath))

    assert len(events) == 2
    assert events[0]["provider"] == "gemini"


def test_calculate_metrics_from_events_all_calls_fail():
    events = [
        {
            "request_id": "aab80e50",
            "timestamp": "2026-10-11T01:57:47.700782+00:00",
            "provider": "gemini",
            "model": "gemini-3.5-flash-lite",
            "tokens_in": 76,
            "tokens_out": 72,
            "latency_ms": 1004.5,
            "ttft_ms": None,
            "cost_usd": 0.00020280000000000002,
            "fallback": True,
            "success": False,
            "error_type": None,
            "prompt_chars": 330,
        },
        {
            "request_id": "eb0812fd",
            "timestamp": "2026-10-11T01:57:55.892567+00:00",
            "provider": "gemini",
            "model": "gemini-3.5-flash-lite",
            "tokens_in": 76,
            "tokens_out": 74,
            "latency_ms": 1072.3,
            "ttft_ms": None,
            "cost_usd": 0.0002078,
            "fallback": True,
            "success": False,
            "error_type": None,
            "prompt_chars": 330,
        },
    ]
    metrics = calculate_metrics_from_events(events)

    assert metrics["calls"] == 2
    assert metrics["fallback_calls_rate"] == 100
    # No quantiles calculations for failed requests
    assert metrics["q_50"] is None
    assert metrics["q_95"] is None


def test_calculate_metrics_from_events_single_call_no_quantiles():
    events = [
        {
            "request_id": "3e5fad42",
            "timestamp": "2026-10-11T20:17:29.847415+00:00",
            "provider": "gemini",
            "model": "gemini-3.5-flash-lite",
            "tokens_in": 76,
            "tokens_out": 64,
            "latency_ms": 1385.5,
            "ttft_ms": None,
            "cost_usd": 0.0001828,
            "fallback": False,
            "success": True,
            "error_type": None,
            "prompt_chars": 330,
        }
    ]

    metrics = calculate_metrics_from_events(events)

    assert metrics["calls"] == 1
    # No quantiles calculations for a single request
    assert metrics["q_50"] is None
    assert metrics["q_95"] is None


def test_calculate_metrics_from_events_single_call_quantiles_values():
    events = [
        {
            "request_id": "aab80e50",
            "timestamp": "2026-10-11T01:57:47.700782+00:00",
            "provider": "gemini",
            "model": "gemini-3.5-flash-lite",
            "tokens_in": 76,
            "tokens_out": 72,
            "latency_ms": 100,
            "ttft_ms": None,
            "cost_usd": 0.00020280000000000002,
            "fallback": False,
            "success": True,
            "error_type": None,
            "prompt_chars": 330,
        },
        {
            "request_id": "73e5c691",
            "timestamp": "2026-10-12T20:44:01.634266+00:00",
            "provider": "groq",
            "model": "openai/gpt-oss-120b",
            "tokens_in": 105,
            "tokens_out": 45,
            "latency_ms": 200,
            "ttft_ms": None,
            "cost_usd": 4.275e-05,
            "fallback": False,
            "success": True,
            "error_type": None,
            "prompt_chars": 129,
        },
        {
            "request_id": "87cc8b1e",
            "timestamp": "2026-10-11T20:03:01.137681+00:00",
            "provider": "gemini",
            "model": "gemini-3.5-flash-lite",
            "tokens_in": 76,
            "tokens_out": 63,
            "latency_ms": 300,
            "ttft_ms": None,
            "cost_usd": 0.00018030000000000002,
            "fallback": False,
            "success": True,
            "error_type": None,
            "prompt_chars": 330,
        },
    ]

    metrics = calculate_metrics_from_events(events)

    assert metrics["calls"] == 3
    assert metrics["q_50"] == 200.0
    assert metrics["q_95"] == 290.0


def test_calculate_metrics_from_events_all_calls_succeed():
    events = [
        {
            "request_id": "aab80e50",
            "timestamp": "2026-10-11T01:57:47.700782+00:00",
            "provider": "gemini",
            "model": "gemini-3.5-flash-lite",
            "tokens_in": 76,
            "tokens_out": 72,
            "latency_ms": 1004.5,
            "ttft_ms": None,
            "cost_usd": 0.00020280000000000002,
            "fallback": False,
            "success": True,
            "error_type": None,
            "prompt_chars": 330,
        },
        {
            "request_id": "73e5c691",
            "timestamp": "2026-10-12T20:44:01.634266+00:00",
            "provider": "groq",
            "model": "openai/gpt-oss-120b",
            "tokens_in": 105,
            "tokens_out": 45,
            "latency_ms": 678.1,
            "ttft_ms": None,
            "cost_usd": 4.275e-05,
            "fallback": False,
            "success": True,
            "error_type": None,
            "prompt_chars": 129,
        },
        {
            "request_id": "87cc8b1e",
            "timestamp": "2026-10-11T20:03:01.137681+00:00",
            "provider": "gemini",
            "model": "gemini-3.5-flash-lite",
            "tokens_in": 76,
            "tokens_out": 63,
            "latency_ms": 1189.0,
            "ttft_ms": None,
            "cost_usd": 0.00018030000000000002,
            "fallback": False,
            "success": True,
            "error_type": None,
            "prompt_chars": 330,
        },
    ]

    metrics = calculate_metrics_from_events(events)

    assert metrics["calls"] == 3
    assert metrics["fallback_calls_rate"] == 0
