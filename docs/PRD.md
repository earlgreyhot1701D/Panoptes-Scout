# Panoptes Scout PRD

## Name

Panoptes Scout

## Tagline

A first pass briefing for any tabular dataset.

## Problem

New and intermediate data workers often feel stuck at the first step with a dataset.

They may:

* Download a CSV and not know what to check first.
* Either run nothing or run every profiling tool they can find.
* Miss obvious issues such as target imbalance, extreme missing values, or impossible values.
* Spend more time on setup than on learning or modeling.

This increases anxiety, wastes hackathon time, and makes learning less enjoyable.

## Solution

Panoptes Scout gives a concise briefing on a tabular dataset before the user writes any code.

It:

* Runs a small set of deterministic profiling checks on a CSV.
* Uses a briefing layer to interpret those statistics.
* Returns a human briefing that highlights the three most important issues and suggested starting moves.

The agent layer will act as a supportive teammate, not an automatic pipeline.

## Primary user

* Learners or hackathon participants who work with tabular data and feel overwhelmed by the initial exploration step.
* Secondary: instructors or mentors who want a repeatable way to show learners how to inspect a dataset.

## Core use cases

1. First contact with a new dataset  
   The user runs Panoptes Scout on a fresh CSV to understand shape, missingness, and target balance.

2. Sanity check before sharing a notebook  
   The user wants to avoid obvious data quality critiques and runs a briefing to catch glaring issues.

3. Teaching tool  
   A mentor uses the output as a conversation starter about why certain issues matter more than others.

## In scope for v1

* Tabular CSV input from local path or URL.
* Simple profiling function that returns:
  * Row and column count.
  * Missing value percentage per column.
  * Duplicate row count.
  * Simple numeric stats for numeric columns.
  * Target distribution when a target column is provided.

* Single briefing layer that:
  * Calls the profiling tool once.
  * Generates a short briefing that includes:
    * Dataset shape.
    * Top three issues ordered by severity.
    * Short list of recommended first actions.
  * Uses clear, beginner friendly language.

* Quality:
  * Three small golden set CSVs and a script that runs the scout on them.
  * README description of how these golden cases support regression checks.

## Out of scope for v1

* Non tabular formats such as images or raw text corpora.
* Automatic plotting or visual dashboards.
* Full RAG stack or BigQuery integration.
* Multi agent delegation or complex model routing.
* Web UI beyond a simple notebook or CLI.

## Functional requirements

1. The scout must always call the profiling tool before generating a briefing.
2. The scout must not invent statistics that are not present in the tool output.
3. If the CSV cannot be read, the scout must surface a clear error in a controlled way.
4. If a target column is provided and present:
   * The scout must report class distribution.
   * The scout must comment on imbalance when any class is under roughly ten percent.

The briefing must be concise enough to read comfortably in a terminal or notebook cell.

## Non functional requirements

* Simple to run from the command line with a single Python command.
* Easy for reviewers to replicate using the instructions in the README.
* Cost aware once Gemini is added, by using a relatively light reasoning model.

## Success indicators

For an intensive or hackathon context, success looks like:

* A working profiling tool and briefing layer that run on multiple example datasets.
* A small golden set that shows how you think about quality.
* A clean path to add Gemini plus ADK while keeping the same public interface.
