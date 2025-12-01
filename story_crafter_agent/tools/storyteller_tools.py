from typing import Dict

def submit_story_with_prompts(story_text: str, image_prompts: Dict[str, str]):
    """
    Submits the generated story text and associated image prompts.
    
    Args:
        story_text: The full text of the story, containing anchors like [IMAGE_1].
        image_prompts: A dictionary mapping anchors (e.g., "IMAGE_1") to image descriptions.
    """
    # In a real agent system, this might save to a context or database.
    # For now, it acts as a structured output for the agent.
    return {
        "story_text": story_text,
        "image_prompts": image_prompts
    }
