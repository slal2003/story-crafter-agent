# Load environment variables FIRST, before importing tools
from dotenv import load_dotenv
from pathlib import Path
import os

env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)
else:
    load_dotenv(override=True)

# Import all tools
from .library_tools import *
from .personalization_tools import *
from .storyteller_tools import *
from .image_generation_tools import *
from .formatting_tools import *

__all__ = [
    'list_available_books',
    'get_book_details',
    'get_book_characters',
    'submit_personalization_profile',
    'submit_story_with_prompts',
    'generate_image',
    'save_formatted_story',
]
