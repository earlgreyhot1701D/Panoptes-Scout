"""
Panoptes Scout ADK agent definition.

This module defines an ADK compatible agent that wraps the existing scout_briefing tool.
It is intentionally small and focused so that it can be inspected during the hackathon.

When you are ready to run this with the ADK CLI:
  1. Move this file into an ADK package directory, for example panoptes_scout_agent/agent.py
  2. Add an __init__.py in that directory with: from .agent import root_agent
  3. Create a .env file with your Google API settings
  4. From the parent directory, run: adk run panoptes_scout_agent
"""

from typing import Optional

from google.adk.agents import LlmAgent

from scout_tool import scout_briefing


SCOUT_INSTRUCTION = """
You are Panoptes Scout, a calm data quality briefing assistant for tabular CSV data.

Your purpose is to:
1. Use the scout_briefing tool to inspect a CSV dataset that lives on disk.
2. Read the returned dictionary of stats and issues.
3. Produce a short, structured briefing for a human data worker.

Output format:
- Begin with a one line overview of the dataset shape.
- Then list any important issues that the scout_briefing tool reports.
- Finish with two or three practical next moves the person can take.

Rules:
- Treat the scout_briefing output as ground truth for counts and basic statistics.
- Do not fabricate column names, counts, or percentages.
- Keep the tone clear and practical, not academic.
"""


root_agent = LlmAgent(
    name="panoptes_scout_agent",
    model="gemini-2.0-flash",  # You can change this to another Gemini model in your env
    description="First pass data quality scout for tabular CSV datasets.",
    instruction=SCOUT_INSTRUCTION,
    tools=[scout_briefing],
)
