# Panoptes Scout: Hackathon Features

## Required Features Demonstrated (3+)

### 1. Custom Tools ✅
**File:** `scout_tool.py` → `scout_briefing()` function

The `scout_briefing` function is a deterministic tool that profiles CSV files.
It takes a CSV path and optional target column, returns structured metrics or
human-readable briefing.

**Why it matters:** Shows understanding of tool design for agents.

### 2. Gemini Model ✅
**File:** `adk_agent.py` → `model="gemini-2.0-flash"`

The agent uses Gemini 2.0 Flash to interpret scout metrics and provide richer
narrative insights.

**Why it matters:** Shows how to integrate LLM models into agent workflows.

### 3. Observability ✅
**File:** `src/logging_config.py` + logging calls in `scout_tool.py`

Structured logging captures each scout operation, metrics discovered, and
results returned.

**Why it matters:** Shows understanding of production-grade observability.

## Bonus Points

### Gemini Use (5 pts) ✅
Uses `gemini-2.0-flash` for analysis enhancement.

### Deployment (5 pts) ⚠️
Not deployed (optional per rubric; focused on code quality instead).

### Video (10 pts) ⚠️
Not included (optional; writeup is better ROI for judging).

## How to Run

```bash
# Test core logic (no Gemini needed)
python golden_tests.py

# Test scout on your own CSV
python -m src.main eval_data/balanced_sample.csv

# Test Gemini integration (requires GOOGLE_API_KEY)
python main_agent.py
```

All tests should pass without deployment.
