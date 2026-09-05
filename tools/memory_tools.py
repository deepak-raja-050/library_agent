from langchain_core.tools import tool
from memory import remember, get_memory


@tool
def save_preference(preference: str) -> str:
    """Save a user's library or book preference for future conversations."""

    remember("user_preference", preference)

    return f"Preference saved: {preference}"


@tool
def get_preferences() -> str:
    """Retrieve the user's saved book and library preferences."""

    memory = get_memory()

    if not memory:
        return "No user preferences have been saved yet."

    return f"Saved preferences: {memory}"