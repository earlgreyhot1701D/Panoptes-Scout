# 👁️ Panoptes Scout

**A first pass data quality briefing agent for tabular datasets**

Named after Argus Panoptes, the all seeing watcher from Greek myth, this scout gives you a calm, opinionated summary before you dive into new data. It is designed for early phase data review and is friendly to agent based workflows.

Panoptes Scout began as a capstone project for the Google AI Agents Intensive Kaggle hackathon in the Enterprise Agents track. The goal is to give both humans and agents a reliable first read on a dataset before anyone starts building models on mystery data.

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
* It gives you a short narrative instead of raw dictionaries  
* It keeps the interface simple enough that an AI agent can call it as a tool  

You get a quick answer to the question  

> Is this dataset in decent shape, and what should I focus on first  

---

## 🧩 Capstone context and agent story

This project was built for the Google AI Agents Intensive capstone as an Enterprise Agent that improves analytics workflows.

Panoptes Scout is intentionally split into three layers.

1. **Scout core**  
   Deterministic Python and pandas logic that profiles a CSV and returns a structured summary.  
   This lives in `src/tools.py` and `src/agent.py`.

2. **Gemini analysis layer**  
   A thin wrapper that turns the summary dictionary into richer commentary for a human data worker using a Gemini model.  
   This lives in `scout_tool.py` and `main_agent.py`.

3. **ADK oriented agent**  
   An agent definition that is shaped to run in the Google Agent Development Kit.  
   It treats `scout_briefing` as a custom tool and provides a clear system instruction for a data quality scout.  
   This lives in `adk_agent.py` and is intended to connect to ADK samples from the course.

Together these pieces demonstrate

* A custom tool that an agent can call  
* An LLM powered agent surface that uses Gemini  
* An ADK compatible agent definition that can be wired to sessions, memory, and observability as shown in the course notebooks  

---

## 🚀 Features

* 📊 Profiles CSV datasets using pandas  
* ⚠️ Highlights missing values, duplicate rows, and class imbalance  
* 💡 Outputs human readable briefings rather than raw dictionaries  
* 🧪 Includes golden test cases under `eval_data`  
* 🤖 Provides a Gemini based analysis layer for richer commentary  
* 🧵 Includes an ADK ready agent definition so Panoptes can live inside a larger agent system  

---

## 🧪 Sample output

```text
📊 Overview
Rows: 1,000 | Columns: 20

⚠️ Issues detected
Column income has 22.1 percent missing values.
Fifteen duplicate rows detected.
Class imbalance Yes has only 8.3 percent of samples.

💡 Recommendations
Consider handling missing values in the highest impact columns.
Investigate and remove exact duplicate rows.
Plan for class imbalance handling in the target variable.
```

Actual wording will vary, but every run follows this pattern  

A short overview, key issues, and concrete starting moves.

---

## 🛠️ Usage

### Install

```bash
pip install -r requirements.txt
```

### Run from the command line

Human scout mode

```bash
python -m src.main path/to/data.csv --target_column label
```

If your dataset has no target column yet, you can skip that flag

```bash
python -m src.main path/to/data.csv
```

### Run golden tests

```bash
python golden_tests.py
```

You will see three briefings, one for each `eval_data` CSV

* A balanced target  
* An imbalanced target  
* Noticeable missing values  

These are tiny but they give you a quick sense of how the scout thinks.

---

## 📂 Project structure

* `src`  
  * `tools.py` contains the profiler function `profile_dataset`  
  * `agent.py` contains the briefing builder and `run_panoptes_scout`  
  * `main.py` exposes the command line entry point  

* `scout_tool.py`  
  * Exposes `scout_briefing` as a tool like interface  
  * Exposes `gemini_analysis` for LLM based commentary  

* `main_agent.py`  
  * Simple runner that calls the scout and Gemini together  

* `adk_agent.py`  
  * Defines an ADK oriented agent configuration that treats `scout_briefing` as a tool  
  * Intended to be wired into the Google ADK samples for full agent runs  

* `eval_data`  
  * Small CSVs used as golden cases  

* `golden_tests.py`  
  * Simple runner that calls the scout on all `eval_data` files  

* `docs/PRD.md` and `docs/MVP.md`  
  * Design notes and scope  

* `requirements.txt`  
  * Python dependencies  

---

## 🤖 Agent modes

Panoptes Scout supports three complementary modes.

### 1. Human mode

Use the command line interface to get a first pass briefing before you build features or models. This is the quickest way to feel how the scout talks about data.

### 2. Gemini helper mode

Use `scout_tool.py` directly in Python to get both a structured summary and Gemini commentary.

```python
from scout_tool import scout_briefing, gemini_analysis

summary = scout_briefing("path/to.csv", "target_column", output_format="json")
readable = scout_briefing("path/to.csv", "target_column", output_format="text")

commentary = gemini_analysis(summary)
print(readable)
print(commentary)
```

This pattern fits agent workflows where a central orchestrator wants both a machine friendly summary and a human ready explanation.

### 3. ADK oriented agent mode

Use `adk_agent.py` as the starting point for a Google ADK agent definition. The file defines an agent instruction and registers the scout tool so the ADK runtime can call it.

In a full ADK setup this agent can be extended with

* Session and memory support as shown in the course  
* Observability hooks for logging and tracing  
* Additional tools such as search or code execution  

The capstone story is that Panoptes Scout is the deterministic foundation that keeps a more complex ADK agent grounded in real data quality checks.

---

## 🧠 Architecture

Panoptes Scout keeps a simple internal structure.

At a high level

+----------------------+        +------------------------+
| CSV file             |   →    | profile_dataset        |
| provided by user     |        |  missing values        |
+----------------------+        |  duplicate rows        |
                                |  numeric statistics    |
                                |  target distribution   |
                                +------------------------+
                                              |
                                              v
                                +------------------------+
                                | build_briefing         |
                                |  overview              |
                                |  key issues            |
                                |  recommendations       |
                                +------------------------+
                                              |
                                              v
                     +------------------------+------------------------+
                     | CLI caller       Gemini helper       ADK agent |
                     +-------------------------------------------------+

Outputs: human readable text briefing and an optional structured summary

Everything beyond this is additive. Gemini, ADK, sessions, and observability can all attach to this core without changing how a user calls it.

---

## ✨ Co builders and tech credits

Panoptes Scout was assembled with a small stack of tools and collaborators

* Python and pandas for deterministic profiling  
* Panoptes as the mythic inspiration for an all seeing scout  
* ChatGPT as code reviewer, refactor helper, and design sounding board  
* Gemini as the analysis layer for richer narrative commentary in `scout_tool.py`  

Future versions are intended to plug into

* Google Agent Development Kit for full agent orchestration  
* Cloud based observability for traces and metrics in real environments  

---

## 📬 Contact and remix

Panoptes Scout started life as a capstone project for the Google AI Agents Intensive Kaggle hackathon.

If you want to extend it, possible directions include

* Adding richer statistics to `profile_dataset`  
* Wiring deeper Gemini based evaluation logic  
* Expanding the ADK agent configuration with sessions, memory, and observability patterns from the course  

Fork it, modify it, and let the many eyed scout keep watch over your datasets.

---

## License

Panoptes Scout is released under the MIT License. See the LICENSE file for details.
