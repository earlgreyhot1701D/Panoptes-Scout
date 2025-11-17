# Panoptes Scout MVP

## MVP statement

A single entry point that takes a CSV path and optional target column, runs one profiling tool, and prints a human readable briefing.

## MVP features

### Input contract

* Required: csv_path as local path or URL.
* Optional: target_column string.

### Profiling tool

Implemented in pure Python using pandas. Returns a dictionary with:

* n_rows
* n_columns
* missing: list with column name and missing percentage.
* duplicates_count
* numeric_stats: list with name, min, max, mean.
* target_info containing:
  * target_column
  * distribution map from class label to count.

### Briefing behavior

* Uses the profiling tool as the only source of quantitative truth.
* Entry point: run_panoptes_scout(csv_path, target_column=None).
* Produces a briefing that includes:
  * One or two sentences describing the dataset.
  * A short list of three main issues.
  * A short list of two or three recommended starting moves.
* Guardrail: explains tool or data errors instead of fabricating output.

### Entry point

* Command line entry:  
  python -m src.main csv_path --target_column label
* Prints the briefing to standard output.

### Golden cases

* Three tiny CSVs under eval_data.
* Script golden_tests.py that calls the scout on each and prints briefings.
