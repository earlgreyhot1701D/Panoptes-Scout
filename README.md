# 👁️ Panoptes Scout

**A first pass data quality briefing agent for tabular datasets**

Named after Argus Panoptes, the all seeing watcher from Greek myth, this scout gives you a calm, opinionated summary before you dive into new data. It is designed for early phase data review and is friendly to future agent based workflows.

---

## ❓ Problem

You open a new CSV and feel that familiar weight in your brain.

* Where do you start
* Is the target balanced
* How bad is missingness
* Are there obvious landmines that will waste hours later

Most people either skip this step or drown in ad hoc checks. The result is fragile work. Models get built on top of shaky data without anyone ever saying that out loud.

Panoptes Scout exists so that the first look at a dataset feels clear, structured, and repeatable instead of foggy and improvisational.

---

## ✅ Solution

Panoptes Scout runs a compact set of deterministic checks, then turns that into a human friendly briefing.

* It profiles your CSV with pandas
* It flags missing values, duplicates, and target imbalance
* It gives you a short narrative instead of raw JSON
* It keeps the interface simple enough that an AI agent can call it as a tool

You get a quick answer to the question: "Is this dataset in decent shape, and what should I focus on first"

---

## 🚀 Features

* 📊 Profiles CSV datasets using pandas
* ⚠️ Highlights missing values, duplicate rows, and class imbalance
* 💡 Outputs human readable briefings rather than raw dictionaries
* 🧪 Includes golden test cases under eval_data
* 🧵 Keeps the summariser layer thin so you can swap in a Gemini agent later

---

## 🧪 Sample Output

```text
📊 Overview
- Rows: 1,000 | Columns: 20

⚠️ Issues Detected
- Column 'income' has 22.1% missing values.
- 15 duplicate rows detected.
- Class imbalance: 'Yes' has only 8.3% of samples.

💡 Recommendations
- Consider handling missing values in top columns.
- Investigate and remove duplicates.
- Address class imbalance in target variable.
```

Actual wording will vary, but every run follows this pattern:
a short overview, key issues, and concrete starting moves.

---

## 🛠️ Usage

### Install

```bash
pip install -r requirements.txt
```

### Run from the command line

```bash
python -m src.main path/to/data.csv --target_column label
```

If your dataset has no target column yet, you can skip that flag:

```bash
python -m src.main path/to/data.csv
```

### Run golden tests

```bash
python golden_tests.py
```

You will see three briefings, one for each eval_data CSV:

* A balanced target
* An imbalanced target
* Noticeable missing values

These are tiny but they give you a quick sense of how the scout thinks.

---

## 📂 Project structure

* `src/`
  * `tools.py` contains the profiler function `profile_dataset`
  * `agent.py` contains the briefing builder and `run_panoptes_scout`
  * `main.py` exposes the command line entry point
* `eval_data/`
  * Small CSVs used as golden cases
* `golden_tests.py`
  * Simple runner that calls the scout on all eval_data files
* `docs/PRD.md` and `docs/MVP.md`
  * Design notes and scope
* `requirements.txt`
  * Python dependencies

---

## 🤖 Agent mode (future ready)

Panoptes Scout is intentionally shaped so that it can become a tool in an AI agent system, for example with the Google Agent Development Kit.

Two modes fit naturally:

1. **Human mode**  
   Use the command line interface to get a briefing before you build features or models.

2. **Agent mode**  
   Wrap `run_panoptes_scout` in a tool definition so that a Gemini powered agent can request a data quality briefing as part of a larger workflow.

A future integration might look like this:

```python
from src.agent import run_panoptes_scout

def scout_briefing_tool(csv_path: str, target_column: str | None = None) -> dict:
    text = run_panoptes_scout(csv_path, target_column)
    return {"briefing": text}
```

An ADK based agent could then call `scout_briefing_tool` whenever it needs a first pass read on a new dataset before it plans the next step.

---

## 🧠 Architecture

Panoptes Scout is intentionally simple.

```text
+----------------------+        +------------------------+
| CSV file             | -----> | profile_dataset()      |
| provided by user     |        |  - missing values      |
+----------------------+        |  - duplicate rows      |
                                |  - numeric statistics  |
                                |  - target distribution |
                                +------------------------+
                                              |
                                              v
                                +------------------------+
                                | build_briefing()       |
                                |  - overview            |
                                |  - key issues          |
                                |  - recommendations     |
                                +------------------------+
                                              |
                                              v
                                +------------------------+
                                | CLI or agent caller    |
                                +------------------------+

Outputs: human readable text briefing
```

Everything beyond this is additive. Gemini, ADK, and Cloud Trace can all attach to this core without changing how a user calls it.

---

## ✨ Co builders and tech credits

Panoptes Scout was assembled with a small stack of tools and collaborators:

* 🛠️ Python and pandas for deterministic profiling
* 👁️ Panoptes as the mythic inspiration for an all seeing scout
* 🤖 ChatGPT as code reviewer, refactor helper, and design sounding board

Future versions are intended to plug into:

* Google Gemini for richer commentary
* Google Agent Development Kit for agent orchestration
* Cloud Trace for observability in real environments

---

## 📬 Contact and remix

Panoptes Scout started life as a capstone style project for an AI agents intensive.

If you want to extend it, possible directions include:

* Adding richer statistics to `profile_dataset`
* Wiring a Gemini summariser that replaces `build_briefing`
* Registering `run_panoptes_scout` as a tool in an ADK based agent

Fork it, modify it, and let the many eyed scout keep watch over your datasets.
