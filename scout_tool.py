from typing import Optional, Literal, Union
import json

from src.tools import profile_dataset
from src.agent import build_briefing
from src.logging_config import get_logger

logger = get_logger("scout_tool")

OutputFormat = Literal["text", "json"]

def scout_briefing(
    csv_path: str,
    target_column: Optional[str] = None,
    output_format: OutputFormat = "text"
) -> Union[str, dict]:
    """
    Analyze a CSV dataset for data quality issues.

    This tool profiles a CSV file and returns either a human-readable briefing
    or structured JSON summary of data quality metrics and issues.

    Design philosophy:
      The scout follows a deterministic-first approach. Core profiling (counts,
      percentages, duplicates) is 100% reproducible. Gemini sits on top for
      narrative enhancement, never inside the logic that produces facts. This
      separation ensures reliability while keeping the agent interface clean.

    Panoptes Scout examines:
    - Dataset shape (rows and columns)
    - Missing values by column (percentage and count)
    - Duplicate rows
    - Numeric column statistics
    - Target variable distribution and class imbalance (if specified)

    Args:
        csv_path (str): Absolute or relative path to the CSV file on disk.
            Example: "/data/customers.csv" or "data/customers.csv"

        target_column (Optional[str]): Name of the target/label column.
            If provided, scout will compute the distribution and check for
            class imbalance. If not found, the tool will note this in output.
            Example: "churn" or "is_fraud"

        output_format (OutputFormat): Output format ('text' or 'json').
            - "text" (default): Human-readable briefing with overview, issues,
              and recommendations
            - "json": Structured dictionary with raw metrics for downstream
              processing

    Returns:
        Union[str, dict]:
            - If output_format="text": String briefing with sections:
              * Dataset overview (rows, columns)
              * Key issues detected (missing, duplicates, imbalance)
              * Suggested starting moves
            - If output_format="json": Dictionary with keys:
              * n_rows, n_columns, missing, duplicates_count, target_info

    Raises:
        FileNotFoundError: If csv_path does not exist or is not readable.
        ValueError: If the CSV cannot be parsed by pandas.

    Example:
        >>> briefing = scout_briefing(
        ...     "data/iris.csv",
        ...     target_column="species",
        ...     output_format="text"
        ... )
        >>> print(briefing)
        Dataset overview: 150 rows and 5 columns...
    """
    logger.info(f"Scout briefing starting for: {csv_path}")

    try:
        summary = profile_dataset(csv_path, target_column)
        logger.info(f"Profiled {summary['n_rows']} rows, {summary['n_columns']} columns")

        if output_format == "json":
            logger.info("Returning JSON format summary")
            return summary

        briefing = build_briefing(summary, target_column)
        logger.info("Scout briefing completed successfully")
        return briefing

    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Error during scout briefing: {str(e)}", exc_info=True)
        raise


# For optional Gemini agent use — generate advice
def gemini_analysis(summary_dict: dict, model_name: str = "gemini-2.0-flash") -> str:
    """
    Uses Gemini to provide analysis or recommendations from the structured scout output.

    Args:
        summary_dict (dict): Output from profile_dataset()
        model_name (str): Gemini model to use (default: gemini-2.0-flash)

    Returns:
        str: Gemini-generated insights

    Raises:
        ImportError: If google-generativeai package is not installed.
        RuntimeError: If Gemini API call fails.
    """
    try:
        from google.generativeai import GenerativeModel
    except ImportError:
        raise ImportError(
            "google-generativeai is required for Gemini analysis. "
            "Install with: pip install google-generativeai"
        )

    try:
        logger.info(f"Starting Gemini analysis with model: {model_name}")
        model = GenerativeModel(model_name)
        prompt = (
            "You are a data scientist assistant."
            " Here is a dictionary of data quality stats from a CSV file."
            " Please write a short, clear briefing of what to look out for, including missing data, duplicates, and class imbalance.\n"
            + json.dumps(summary_dict)
        )
        response = model.generate_content(prompt)
        logger.info("Gemini analysis completed successfully")
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}", exc_info=True)
        raise RuntimeError(
            f"Gemini analysis failed: {str(e)}. "
            f"This may be a network issue or API rate limit."
        )