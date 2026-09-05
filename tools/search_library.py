from langchain_core.tools import tool
import sqlite3

DB_NAME = "library.db"


@tool
def search_library(query: str) -> str:
    """Search the library database for books by title, author, or category."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    search_term = f"%{query}%"

    cursor.execute("""
        SELECT id, title, author, category, available
        FROM books
        WHERE title LIKE ?
           OR author LIKE ?
           OR category LIKE ?
    """, (search_term, search_term, search_term))

    results = cursor.fetchall()
    conn.close()

    if not results:
        return "No books found matching the search."

    output = []

    for book in results:
        book_id, title, author, category, available = book

        status = "Available" if available else "Not Available"

        output.append(
            f"ID: {book_id} | "
            f"Title: {title} | "
            f"Author: {author} | "
            f"Category: {category} | "
            f"Status: {status}"
        )

    return "\n".join(output)