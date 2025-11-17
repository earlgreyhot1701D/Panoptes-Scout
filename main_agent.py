from scout_tool import scout_briefing, gemini_analysis
from typing import Optional

def run_agent_on_csv(csv_path: str, target_column: Optional[str] = None):
    """
    Runs the Panoptes Scout as an agentic tool on a CSV file.
    Optionally calls Gemini to generate follow-up suggestions.
    """
    print("🔍 Running scout_briefing...\n")
    summary = scout_briefing(csv_path, target_column, output_format="json")
    readable = scout_briefing(csv_path, target_column, output_format="text")

    print(readable)

    print("\n🧠 Calling Gemini for expert-level suggestions...\n")
    try:
        gemini_opinion = gemini_analysis(summary)
        print(gemini_opinion)
    except Exception as e:
        print("[WARNING] Gemini call failed:", e)


if __name__ == "__main__":
    run_agent_on_csv("eval_data/imbalanced_sample.csv", "label")