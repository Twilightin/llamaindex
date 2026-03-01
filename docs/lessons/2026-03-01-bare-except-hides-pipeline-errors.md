# Never use bare `except Exception` around pipeline.load()

**Date:** 2026-03-01

## What Happened

`IngestionPipeline.load()` was wrapped in a bare `except Exception` to handle the "first run" case where no cache exists yet. This looks harmless but silently swallows any real error — a corrupted cache file, a permissions problem, or a full disk — and prints "starting fresh" as if nothing happened.

```python
# What NOT to do
try:
    pipeline.load(pipeline_storage)
except Exception:
    print("No existing pipeline cache found — starting fresh.")
```

## Why It's a Problem

When the cache *exists but fails to load* for a real reason, the pipeline discards its deduplication state. Every document gets re-embedded from scratch on the next run — wasting OpenAI API calls and time. The user sees "starting fresh" with no clue that something went wrong. The bug is silent and expensive.

## Fix / Do This Instead

```python
# Catch only what you expect: file doesn't exist yet, or cache is unreadable
try:
    pipeline.load(PIPELINE_DIR)
    print("Loaded existing pipeline cache from storage.")
except (FileNotFoundError, ValueError):
    print("No existing pipeline cache found — starting fresh.")
```

`FileNotFoundError` covers the legitimate first-run case. `ValueError` covers a corrupted or incompatible cache format. Any other exception (permissions, disk full, memory) will now propagate correctly and be visible.

## Prevention

Only catch the specific exceptions you expect — never use bare `except Exception` as a "just in case" catch-all around stateful operations.
