"""
StoryTeller Agent

Generates personalized story adaptations of classic literature with illustration prompts.
- Adapts vocabulary, tone, and length to target audience
- Structures content into flowing Parts (not chapters)
- Creates image prompts for key story moments
"""

from pathlib import Path
from google.adk.agents import Agent
from google.adk.tools import transfer_to_agent
from story_crafter_agent.tools.library_tools import get_book_details
from story_crafter_agent.tools.storyteller_tools import submit_story_with_prompts


def _load_prompt_file(filename: str) -> str:
    """Load prompt text from the prompts directory."""
    file_path = Path(__file__).parent.parent / "prompts" / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


storyteller_agent = Agent(
    name="StoryTellerAgent",
    model="gemini-2.5-pro",
    instruction=_load_prompt_file("storyteller_agent.md"),
    tools=[get_book_details, submit_story_with_prompts, transfer_to_agent],
    description="Generates personalized illustrated story adaptations from classic literature"
)
