
import pandas as pd

IMBALANCE_THRESHOLD = 0.10  # Flag if any class is <10% of target distribution

def profile_dataset(csv_path: str, target_column: str | None = None) -> dict:
    """
    Profile a CSV dataset for data quality metrics.

    Args:
        csv_path: Path to CSV file
        target_column: Optional target column name for distribution analysis

    Returns:
        dict: Profiling statistics
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Failed to parse CSV {csv_path}. Details: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error reading {csv_path}: {str(e)}")

    n_rows, n_columns = df.shape

    missing = (
        df.isna()
        .mean()
        .reset_index()
        .rename(columns={"index": "column", 0: "missing_pct"})
        .to_dict(orient="records")
    )

    duplicates_count = int(df.duplicated().sum())

    numeric_stats = []
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

    target_info = None
    if target_column and target_column in df.columns:
        counts = df[target_column].value_counts(dropna=False)
        proportions = counts / counts.sum()
        is_imbalanced = proportions.min() < IMBALANCE_THRESHOLD
        target_info = {
            "target_column": target_column,
            "distribution": counts.to_dict(),
            "is_imbalanced": bool(is_imbalanced),
        }

    return {
        "n_rows": int(n_rows),
        "n_columns": int(n_columns),
        "missing": missing,
        "duplicates_count": duplicates_count,
        "numeric_stats": numeric_stats,
        "target_info": target_info,
    }
