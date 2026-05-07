# Logging

## Overview

CodeSurgeon uses structured logging with Loguru for observability and debugging.

## Log Levels

- **DEBUG:** Detailed information for diagnosing problems (LLM API calls, cache hits/misses)
- **INFO:** General informational messages (startup, request count)
- **WARNING:** Warning messages for potentially problematic situations
- **ERROR:** Error messages for serious issues
- **CRITICAL:** Critical failures that may cause shutdown

## Configuration

Set log level in `.env`:

```bash
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

Or via environment variable:

```bash
LOG_LEVEL=DEBUG python -m uvicorn src/myproject/api:app --host 0.0.0.0 --port 8000
```

## Log Format

All logs follow this format:

```
2026-05-07T10:30:45.123Z | INFO     | [module:function:line] message
```

Example:

```
2026-05-07T10:30:45.123Z | INFO     | [api:analyze:45] POST /api/v1/analyze - analyzing code, language=python
2026-05-07T10:30:47.456Z | DEBUG    | [llm_client:call_llm:78] LLM request: prompt_tokens=150, model=claude-3-opus
2026-05-07T10:30:48.789Z | DEBUG    | [bug_detector:detect_bugs:112] Detected 2 bugs (recall: 82%)
2026-05-07T10:30:48.790Z | INFO     | [api:analyze:46] Response: 2 bugs, latency_ms=2667
```

## Structured Logging Fields

Every log entry includes:

- `timestamp`: ISO 8601 format
- `level`: Log level
- `module`: Source module name
- `function`: Function name
- `line`: Line number
- `request_id`: UUID for request tracing (if applicable)
- `user_agent`: Browser/client info (API logs only)
- `message`: Log message

## Request Tracing Example

Trace a single request from start to finish:

```bash
# Enable DEBUG logging
LOG_LEVEL=DEBUG python -m uvicorn src/myproject/api:app

# Make a request (in another terminal)
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "x = 1 || 2", "language": "python"}'
```

Expected logs:

```
2026-05-07T10:30:45.001Z | INFO     | [api:analyze:45] POST /api/v1/analyze | request_id=abc-123
2026-05-07T10:30:45.002Z | DEBUG    | [api:analyze:47] Input: code_length=11, language=python | request_id=abc-123
2026-05-07T10:30:45.003Z | DEBUG    | [code_analyzer:analyze:22] Parsing Python code | request_id=abc-123
2026-05-07T10:30:45.100Z | DEBUG    | [bug_detector:detect_bugs:50] Running static analysis | request_id=abc-123
2026-05-07T10:30:45.101Z | DEBUG    | [bug_detector:_static_analysis:78] Found 1 pattern match: || operator | request_id=abc-123
2026-05-07T10:30:45.102Z | DEBUG    | [llm_client:call_llm:200] LLM request starting | request_id=abc-123 | model=claude-3-opus | prompt_tokens=250
2026-05-07T10:30:47.450Z | DEBUG    | [llm_client:call_llm:210] LLM response received | request_id=abc-123 | completion_tokens=180 | latency_ms=2348
2026-05-07T10:30:47.460Z | DEBUG    | [bug_detector:detect_bugs:90] LLM returned 1 bug | request_id=abc-123
2026-05-07T10:30:47.461Z | DEBUG    | [bug_detector:_deduplicate_bugs:120] Deduplicated to 1 unique bug | request_id=abc-123
2026-05-07T10:30:47.470Z | INFO     | [api:analyze:55] Response: 1 bug | request_id=abc-123 | latency_ms=2469
```

## Log Files

Logs are written to:

- **Console:** Always (STDERR)
- **File:** `logs/app.log` (rotated daily, 7-day retention)

Configure in `src/myproject/logger.py`:

```python
logger.add(
    "logs/app.log",
    rotation="00:00",  # Daily rotation at midnight
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
)
```

## Sensitive Data Handling

**Do NOT log:**
- API keys (ANTHROPIC_API_KEY, OPENAI_API_KEY, GITHUB_TOKEN)
- User code (unless LOG_LEVEL=DEBUG and code_length <100 chars)
- Passwords or credentials

**Safe to log:**
- Request metadata (URL, method, latency)
- Error messages and stack traces
- Configuration (non-secret values)

## Monitoring and Alerts

Example Prometheus metrics (if enabled):

```
# HELP codesurgeon_api_requests_total Total API requests
# TYPE codesurgeon_api_requests_total counter
codesurgeon_api_requests_total{method="POST",endpoint="/api/v1/analyze"} 1234

# HELP codesurgeon_latency_seconds Request latency
# TYPE codesurgeon_latency_seconds histogram
codesurgeon_latency_seconds_bucket{le="1"} 100
codesurgeon_latency_seconds_bucket{le="5"} 1200
codesurgeon_latency_seconds_bucket{le="+Inf"} 1234
codesurgeon_latency_seconds_sum 4200
codesurgeon_latency_seconds_count 1234
```

## Troubleshooting with Logs

**Problem:** API timeout

```bash
grep "timeout" logs/app.log | tail -20
# Look for "LLM timeout" or "GitHub API timeout"
```

**Problem:** 500 errors

```bash
grep "ERROR\|CRITICAL" logs/app.log | tail -20
# Look for stack traces
```

**Problem:** High latency

```bash
grep "latency_ms" logs/app.log | awk -F'latency_ms=' '{print $2}' | sort -rn | head -10
# Top 10 slowest requests
```

---

**Last updated:** May 7, 2026
