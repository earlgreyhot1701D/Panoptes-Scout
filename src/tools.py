import pandas as pd


def profile_dataset(csv_path: str, target_column: str | None = None) -> dict:
    """Load a CSV file and compute simple profiling statistics.

    The function returns a dictionary with:
    * n_rows and n_columns
    * missing: list of dictionaries with column and missing_pct
    * duplicates_count: number of duplicate rows
    * numeric_stats: list of dictionaries with basic stats for numeric columns
    * target_info: target column name and class distribution if provided
    """

    df = pd.read_csv(csv_path)

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
