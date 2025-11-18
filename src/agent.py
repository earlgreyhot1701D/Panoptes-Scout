from typing import Any

from .tools import profile_dataset


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
        List of dictionaries for columns with missing values, sorted by percentage
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

    Args:
        target_info: Dictionary with 'distribution' key containing class counts

    Returns:
        Dictionary with min_class, min_pct, and is_imbalanced (threshold: 10%)
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
        "is_imbalanced": min_pct < 0.1,
    }


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

    n_rows = summary.get("n_rows", 0)
    n_columns = summary.get("n_columns", 0)
    missing = summary.get("missing", [])
    duplicates_count = summary.get("duplicates_count", 0)
    target_info = summary.get("target_info")

    lines: list[str] = []

    # Overview
    lines.append(
        f"Dataset overview: {n_rows} rows and {n_columns} columns in a tabular CSV."
    )

    # Main issues
    issues: list[str] = []

    top_missing = _pick_top_missing(missing)
    if top_missing:
        cols_desc = ", ".join(
            f"{c['column']} ({_format_percentage(c['missing_pct'])} missing)"
            for c in top_missing
        )
        issues.append(
            "Columns with missing values: " + cols_desc + "."
        )

    if duplicates_count > 0:
        issues.append(
            f"There are {duplicates_count} duplicate rows that may need review or removal."
        )

    imb = _compute_imbalance(target_info)
    if imb and imb.get("is_imbalanced"):
        issues.append(
            "Target imbalance detected: class "
            + str(imb["min_class"])
            + " has only "
            + _format_percentage(imb["min_pct"])
            + " of the examples."
        )

    if not issues:
        issues.append(
            "No severe data quality problems were detected by the simple profiler."
        )

    lines.append("\nKey issues:")
    for idx, issue in enumerate(issues, start=1):
        lines.append(f"{idx}. {issue}")

    # Recommendations
    recs: list[str] = []

    if top_missing:
        recs.append(
            "Decide how to handle the highest missing value columns. You can drop them, impute them, or treat missing as its own category."
        )
    if duplicates_count > 0:
        recs.append(
            "Inspect duplicates to see whether they are true repeats or valid multiple records, then drop the ones that do not belong."
        )
    if imb and imb.get("is_imbalanced"):
        recs.append(
            "Plan for target imbalance before modeling. Sampling, class weights, or appropriate metrics can help."
        )
    recs.append(
        "Create a quick notebook with a few simple plots or value counts to verify these findings and look for obvious outliers."
    )

    lines.append("\nSuggested starting moves:")
    for idx, rec in enumerate(recs, start=1):
        lines.append(f"{idx}. {rec}")

    if target_column and not target_info:
        lines.append(
            f"Note: target_column='{target_column}' was provided but that column name was not found in the CSV."
        )

    return "\n".join(lines)


def run_panoptes_scout(csv_path: str, target_column: str | None = None) -> str:
    """
    Entry point for Panoptes Scout.

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
