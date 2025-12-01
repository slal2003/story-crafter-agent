"""Subagents for the illustrated story crafter agent."""

# Load environment variables FIRST, before importing agents
from dotenv import load_dotenv
from pathlib import Path
import os

env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)
else:
    load_dotenv(override=True)

from .library_agent import library_agent
from .personalization_agent import personalization_agent
from .storyteller_agent import storyteller_agent
from .illustration_agent import illustration_agent
from .formatter_agent import formatter_agent

__all__ = [
    'library_agent',
    'personalization_agent',
    'storyteller_agent',
    'illustration_agent',
    'formatter_agent'
]

