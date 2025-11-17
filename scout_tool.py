from typing import Optional, Literal, Union
import json

from src.tools import profile_dataset
from src.agent import build_briefing

OutputFormat = Literal["text", "json"]

def scout_briefing(
    csv_path: str,
    target_column: Optional[str] = None,
    output_format: OutputFormat = "text"
) -> Union[str, dict]:
    """
    Tool function to run a data quality briefing on a CSV.

    Args:
        csv_path (str): Path to the CSV file.
        target_column (Optional[str]): Target column name.
        output_format (str): 'text' or 'json' output mode.

    Returns:
        str | dict: Briefing text or structured dictionary summary.
    """
    summary = profile_dataset(csv_path, target_column)

    if output_format == "json":
        return summary

    return build_briefing(summary, target_column)


# For optional Gemini agent use — generate advice
from google.generativeai import GenerativeModel

def gemini_analysis(summary_dict: dict, model_name: str = "gemini-pro") -> str:
    """
    Uses Gemini to provide analysis or recommendations from the structured scout output.

    Args:
        summary_dict (dict): Output from profile_dataset()
        model_name (str): Gemini model to use

    Returns:
        str: Gemini-generated insights
    """
    model = GenerativeModel(model_name)
    prompt = (
        "You are a data scientist assistant."
        " Here is a dictionary of data quality stats from a CSV file."
        " Please write a short, clear briefing of what to look out for, including missing data, duplicates, and class imbalance.\n"
        + json.dumps(summary_dict)
    )
    response = model.generate_content(prompt)
    return response.text