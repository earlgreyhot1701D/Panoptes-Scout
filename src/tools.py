import pandas as pd


def profile_dataset(csv_path: str, target_column: str | None = None) -> dict:
    """
    Profile a CSV dataset for data quality metrics.

    Design: This function is intentionally deterministic and side-effect free.
    It reads a CSV into pandas and gathers statistics without any LLM calls.
    This makes it reliable, testable, and cacheable. Higher-level functions
    (briefing builders, Gemini helpers) can interpret these facts without
    worrying about non-determinism.

    Returns a dictionary with:
    - n_rows, n_columns: Dataset shape
    - missing: List of columns with missing values
    - duplicates_count: Number of duplicate rows
    - numeric_stats: List of dictionaries with basic stats for numeric columns
    - target_info: Distribution of target column (if provided)

    Args:
        csv_path: Path to CSV file
        target_column: Optional target column name for distribution analysis

    Returns:
        dict: Profiling statistics

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV cannot be parsed
        RuntimeError: For other unexpected errors
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}\n"
            f"Please check the path and try again."
        )
    except pd.errors.ParserError as e:
        raise ValueError(
            f"Failed to parse CSV {csv_path}. "
            f"Ensure it's valid CSV format.\n"
            f"Details: {str(e)}"
        )
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error reading {csv_path}: {str(e)}"
        )

    n_rows, n_columns = df.shape

    # Missing value percentage per column
    missing = (
        df.isna()
        .mean()
        .reset_index()
        .rename(columns={"index": "column", 0: "missing_pct"})
        .to_dict(orient="records")
    )

    # Duplicate row count
    duplicates_count = int(df.duplicated().sum())

    # Simple numeric stats
    numeric_stats: list[dict] = []
    for col in df.select_dtypes(include="number").columns:
        series = df[col]
        numeric_stats.append(
            {
                "name": col,
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": float(series.mean()),
            }
        )

    # Target distribution when target column is present
    target_info: dict | None = None
    if target_column and target_column in df.columns:
        counts = df[target_column].value_counts(dropna=False).to_dict()
        target_info = {
            "target_column": target_column,
            "distribution": {str(k): int(v) for k, v in counts.items()},
        }

    return {
        "n_rows": int(n_rows),
        "n_columns": int(n_columns),
        "missing": missing,
        "duplicates_count": duplicates_count,
        "numeric_stats": numeric_stats,
        "target_info": target_info,
    }
