"""
Library Tools

Tools for interacting with the Phase 1 Book Summaries API.
"""

import os
import httpx
from google.adk.tools import FunctionTool
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_BASE_URL = "http://127.0.0.1:8010"
API_KEY = os.getenv("PHASE1_API_KEY", "")

def _get_headers() -> Dict[str, str]:
    headers = {"accept": "application/json"}
    if API_KEY:
        headers["x-api-key"] = API_KEY
    return headers

@FunctionTool
def list_available_books(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get a list of all available books in the library via the API.
    
    Args:
        category: Optional category filter (e.g., 'Fantasy', 'Fiction').
    
    Returns:
        List of books with id, title, author, genre, and overview.
    """
    try:
        params = {}
        if category:
            params["category"] = category
            
        with httpx.Client() as client:
            response = client.get(
                f"{API_BASE_URL}/books", 
                headers=_get_headers(),
                params=params
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return [{"error": f"Failed to fetch books from API: {str(e)}"}]

@FunctionTool
def get_book_details(book_id: str) -> Dict[str, Any]:
    """
    Get the full details and summary of a specific book from the API.
    
    Args:
        book_id: The ID of the book to retrieve.
        
    Returns:
        Complete book summary including plot, characters, and themes.
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{API_BASE_URL}/books/{book_id}",
                headers=_get_headers()
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch book details: {str(e)}"}

@FunctionTool
def get_book_characters(book_id: str) -> List[Dict[str, Any]]:
    """
    Get just the list of characters for a specific book.
    
    Args:
        book_id: The ID of the book.
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{API_BASE_URL}/books/{book_id}/characters",
                headers=_get_headers()
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return [{"error": f"Failed to fetch characters: {str(e)}"}]
