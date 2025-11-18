from typing import Any

from .tools import profile_dataset, IMBALANCE_THRESHOLD


def _format_percentage(p: float) -> str:
    """Format a decimal as a percentage string."""
    return f"{p * 100:.1f}%"


def _pick_top_missing(missing_list: list[dict], top_n: int = 3) -> list[dict]:
    """
    Pick top N columns with missing values.

    Args:
        missing_list: List of dictionaries with 'column' and 'missing_pct' keys
        top_n: Number of top missing columns to return

    Returns:
        List of dictionaries for columns with missing values, sorted by percentage descending
    """
    sorted_cols = sorted(
        missing_list,
        key=lambda c: c.get("missing_pct", 0.0),
        reverse=True,
    )
    return [c for c in sorted_cols if c.get("missing_pct", 0.0) > 0][:top_n]


def _compute_imbalance(target_info: dict | None) -> dict | None:
    """
    Compute class imbalance statistics.

    Uses the IMBALANCE_THRESHOLD from tools.py to ensure consistency across the system.

    Args:
        target_info: Dictionary with 'distribution' key containing class counts

    Returns:
        Dictionary with:
            - min_class: The class with fewest examples
            - min_pct: Percentage of minority class
            - is_imbalanced: Boolean (True if minority < IMBALANCE_THRESHOLD)
        Returns None if no valid target info provided
    """
    if not target_info:
        return None
    
    dist = target_info.get("distribution", {})
    if not dist:
        return None
    
    total = sum(dist.values())
    if total == 0:
        return None
    
    percentages = {k: v / total for k, v in dist.items()}
    min_class = min(percentages, key=percentages.get)
    min_pct = percentages[min_class]
    
    return {
        "min_class": min_class,
        "min_pct": min_pct,
        "is_imbalanced": min_pct < IMBALANCE_THRESHOLD,
    }


def _build_issues(summary: dict) -> list[str]:
    """
    Extract data quality issues from profiling summary.

    Args:
        summary: Dictionary from profile_dataset with data quality metrics

    Returns:
        List of issue strings to display to user
    """
    issues: list[str] = []
    
    missing = summary.get("missing", [])
    duplicates_count = summary.get("duplicates_count", 0)
    target_info = summary.get("target_info")

    # Check for missing values
    top_missing = _pick_top_missing(missing)
    if top_missing:
        cols_desc = ", ".join(
            f"{c['column']} ({_format_percentage(c['missing_pct'])} missing)"
            for c in top_missing
        )
        issues.append("Columns with missing values: " + cols_desc + ".")

    # Check for duplicates
    if duplicates_count > 0:
        issues.append(
            f"There are {duplicates_count} duplicate rows that may need review or removal."
        )

    # Check for class imbalance
    imb = _compute_imbalance(target_info)
    if imb and imb.get("is_imbalanced"):
        issues.append(
            "Target imbalance detected: class "
            + str(imb["min_class"])
            + " has only "
            + _format_percentage(imb["min_pct"])
            + " of the examples."
        )

    # Default if no issues found
    if not issues:
        issues.append(
            "No severe data quality problems were detected by the simple profiler."
        )

    return issues


def _build_recommendations(summary: dict) -> list[str]:
    """
    Generate recommended next steps based on identified issues.

    Args:
        summary: Dictionary from profile_dataset with data quality metrics

    Returns:
        List of recommendation strings
    """
    recs: list[str] = []
    
    missing = summary.get("missing", [])
    duplicates_count = summary.get("duplicates_count", 0)
    target_info = summary.get("target_info")

    # Recommendations for missing values
    top_missing = _pick_top_missing(missing)
    if top_missing:
        recs.append(
            "Decide how to handle the highest missing value columns. You can drop them, impute them, or treat missing as its own category."
        )

    # Recommendations for duplicates
    if duplicates_count > 0:
        recs.append(
            "Inspect duplicates to see whether they are true repeats or valid multiple records, then drop the ones that do not belong."
        )

    # Recommendations for imbalance
    imb = _compute_imbalance(target_info)
    if imb and imb.get("is_imbalanced"):
        recs.append(
            "Plan for target imbalance before modeling. Sampling, class weights, or appropriate metrics can help."
        )

    # General recommendation (always included)
    recs.append(
        "Create a quick notebook with a few simple plots or value counts to verify these findings and look for obvious outliers."
    )

    return recs


def build_briefing(summary: dict, target_column: str | None = None) -> str:
    """
    Build a human-friendly narrative briefing from raw profiling stats.

    Design: This function translates the raw summary dictionary (rows,
    columns, counts, percentages) into a structured narrative with three
    sections: overview, key issues, and recommended next moves.

    The output is intentionally short and scannable—analysts should
    understand the main risks in 30 seconds. This keeps cognitive load low,
    which is the core value proposition of Panoptes Scout.

    Args:
        summary: Dictionary from profile_dataset with data quality metrics
        target_column: Optional target column name for context in warnings

    Returns:
        Human-readable briefing with overview, issues, and recommendations
    """
    lines: list[str] = []

    # Overview section
    n_rows = summary.get("n_rows", 0)
    n_columns = summary.get("n_columns", 0)
    lines.append(
        f"Dataset overview: {n_rows} rows and {n_columns} columns in a tabular CSV."
    )

    # Key issues section
    issues = _build_issues(summary)
    lines.append("\nKey issues:")
    for idx, issue in enumerate(issues, start=1):
        lines.append(f"{idx}. {issue}")

    # Recommended actions section
    recs = _build_recommendations(summary)
    lines.append("\nSuggested starting moves:")
    for idx, rec in enumerate(recs, start=1):
        lines.append(f"{idx}. {rec}")

    # Note if target column was requested but not found
    target_info = summary.get("target_info")
    if target_column and not target_info:
        lines.append(
            f"\nNote: target_column='{target_column}' was provided but that column name was not found in the CSV."
        )

    return "\n".join(lines)


def run_panoptes_scout(csv_path: str, target_column: str | None = None) -> str:
    """
    Entry point for Panoptes Scout.

    Orchestrates the data profiling and briefing generation workflow.
    For now this uses a deterministic briefing builder on top of the profiling tool.
    Gemini and the ADK can replace the briefing layer later without changing this
    function signature.

    Args:
        csv_path: Path to CSV file to analyze
        target_column: Optional name of target/label column

    Returns:
        Human-readable briefing string
    """
    summary = profile_dataset(csv_path=csv_path, target_column=target_column)
    return build_briefing(summary, target_column=target_column)
