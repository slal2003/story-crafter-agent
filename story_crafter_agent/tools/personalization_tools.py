"""
Personalization Tools

Tools for capturing user preferences.
"""

from google.adk.tools import FunctionTool
from typing import List, Dict, Any, Optional

@FunctionTool
def submit_personalization_profile(
    audience: str,
    tone: str,
    length: str,
    originality_score: float,
    special_adaptations: List[str],
    book_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Submit the final personalization profile after the interview is complete.
    
    Args:
        audience: Target audience (e.g., 'Child 5-8', 'Teen', 'Adult').
        tone: Desired tone (e.g., 'Whimsical', 'Serious').
        length: Desired length (e.g., 'Short', 'Medium').
        originality_score: 0.0 to 1.0 (0=highly adapted, 1=faithful).
        special_adaptations: List of specific adaptation requests.
        book_id: The book ID selected from the library (e.g., '2701' for Moby-Dick).
        
    Returns:
        The confirmed profile dictionary.
    """
    return {
        "audience": audience,
        "tone": tone,
        "length": length,
        "originality_score": originality_score,
        "special_adaptations": special_adaptations,
        "book_id": book_id,
        "status": "confirmed"
    }
