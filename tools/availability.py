from langchain_core.tools import tool
import sqlite3

DB_NAME = "library.db"


@tool
def check_availability(book_title: str) -> str:
    """Check whether a specific book is currently available in the library."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, author, available
        FROM books
        WHERE title LIKE ?
    """, (f"%{book_title}%",))

    results = cursor.fetchall()
    conn.close()

    if not results:
        return f"Book '{book_title}' was not found in the library."

    output = []

    for title, author, available in results:
        if available:
            status = "Available for borrowing"
        else:
            status = "Currently borrowed"

        output.append(
            f"Title: {title} | Author: {author} | Status: {status}"
        )

    return "\n".join(output)