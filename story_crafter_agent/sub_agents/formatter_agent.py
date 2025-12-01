"""
Formatter Agent

Transforms raw story with image anchors into a polished, book-like illustrated story.
- Restructures content from chapters to logical Parts
- Replaces image anchors with proper markdown
- Applies book-like styling and formatting
"""

from pathlib import Path
from google.adk.agents import Agent
from story_crafter_agent.tools.formatting_tools import save_formatted_story


def _load_prompt_file(filename: str) -> str:
    """Load prompt text from the prompts directory."""
    file_path = Path(__file__).parent.parent / "prompts" / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


formatter_agent = Agent(
    name="FormatterAgent",
    model="gemini-2.5-pro",
    instruction=_load_prompt_file("formatter_agent.md"),
    tools=[save_formatted_story],
    description="Formats and polishes the illustrated story into a book-like presentation"
)
