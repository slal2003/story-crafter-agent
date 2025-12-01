"""
Main root agent for Illustrated Literature Agents.

This root agent coordinates subagents to provide personalized illustrated summaries
of classic literature from Project Gutenberg.
"""

# Load environment variables FIRST, before any ADK imports
from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env from project root
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)
else:
    # Fallback: try current directory
    load_dotenv(override=True)

# Verify configuration is loaded (for debugging)
use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").upper() in ("1", "TRUE", "YES", "Y")
api_key = os.getenv("GOOGLE_API_KEY")

if use_vertex:
    print("✓ Using Vertex AI backend (GOOGLE_GENAI_USE_VERTEXAI is set)")
    print("  Note: Vertex AI uses Google Cloud billing and Application Default Credentials")
elif api_key:
    # Log that key is loaded (without exposing the actual key)
    print(f"✓ Using Gemini API backend - API Key loaded from .env (length: {len(api_key)} chars)")
else:
    import warnings
    warnings.warn(
        f"⚠️ Neither Vertex AI nor API key configured!\n"
        f"   For Vertex AI: Set GOOGLE_GENAI_USE_VERTEXAI=1 in .env\n"
        f"   For Gemini API: Set GOOGLE_API_KEY=your-key in .env\n"
        f"   Checked .env file at: {env_file}"
    )

# NOW import ADK (after env vars are loaded)
from google.adk.agents import Agent

from story_crafter_agent.sub_agents.library_agent import library_agent
from story_crafter_agent.sub_agents.personalization_agent import personalization_agent
from story_crafter_agent.sub_agents.storyteller_agent import storyteller_agent
from story_crafter_agent.sub_agents.illustration_agent import illustration_agent
from story_crafter_agent.sub_agents.formatter_agent import formatter_agent


# Load prompt file
_PROMPTS_DIR = Path(__file__).parent / "prompts"


def _load_prompt_file(filename: str) -> str:
    """Load prompt text from the prompts directory."""
    file_path = _PROMPTS_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


# Main root agent definition
# This agent coordinates the simplified MVP flow
root_agent = Agent(
    name="StoryCrafterAgent",
    model="gemini-2.0-flash-exp",
    instruction=_load_prompt_file("root_agent_mvp.md"),
    tools=[],  # Root agent coordinates sub-agents
    sub_agents=[
        library_agent,          # Step 1: Find books
        personalization_agent,  # Step 2: Get user preferences
        storyteller_agent,      # Step 3: Generate story
        illustration_agent,     # Step 4: Generate images
        formatter_agent         # Step 5: Format output
    ],
)
