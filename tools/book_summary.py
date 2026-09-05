from langchain_core.tools import tool

@tool
def book_summary(book_title: str) -> str:
    """Provide a concise summary of a book."""

    summaries = {
        "python crash course":
            "Python Crash Course is a beginner-friendly introduction to Python programming. "
            "It covers programming fundamentals and then applies them through practical projects.",

        "clean code":
            "Clean Code by Robert C. Martin explains principles and practices for writing "
            "readable, maintainable, and understandable software.",

        "the pragmatic programmer":
            "The Pragmatic Programmer presents practical principles for improving software "
            "development, problem solving, design, testing, and maintainability.",

        "hands-on machine learning":
            "Hands-On Machine Learning introduces machine learning concepts and practical "
            "implementation using popular Python-based machine learning tools."
    }

    key = book_title.lower().strip()

    if key in summaries:
        return summaries[key]

    return (
        f"No stored summary is available for '{book_title}'. "
        "Use web_search to find information about this book."
    )