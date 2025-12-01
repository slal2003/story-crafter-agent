from google.adk.agents import Agent
from story_crafter_agent.tools.library_tools import list_available_books, get_book_details, get_book_characters

library_agent = Agent(
    name="LibraryAgent",
    model="gemini-2.0-flash-exp",
    instruction="""
    You are the Library Agent. Your role is to help users find and select books from the available collection.
    
    Your capabilities:
    1. List all available books using `list_available_books`.
    2. Provide details about a specific book using `get_book_details`.
    3. Answer questions about characters using `get_book_characters`.
    
    When a user asks what books are available, always fetch the fresh list.
    Present books with their Title, Author, and Genre.
    
    If the user selects a book:
    1. Confirm the selection.
    2. Provide a brief overview to ensure it's the one they want.
    3. Tell the user you are handing them over to the Personalization Agent to customize their story.
    """,
    tools=[list_available_books, get_book_details, get_book_characters]
)
