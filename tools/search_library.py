from langchain_core.tools import tool
import sqlite3

DB_NAME = "library.db"

@tool
def search_library(query: str) -> str:
    """Search the library database for books by title, author, or category.
    If the user asks for all available books, return every currently available book.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Handle request for all available books
    if query.lower().strip() in [
        "all available books",
        "available books",
        "all books available",
        "books that are available",
        "what books are available"
    ]:
        cursor.execute("""
            SELECT id, title, author, category
            FROM books
            WHERE available = 1
        """)

        results = cursor.fetchall()
        conn.close()

        if not results:
            return "There are currently no available books."

        output = []

        for book_id, title, author, category in results:
            output.append(
                f"ID: {book_id} | "
                f"Title: {title} | "
                f"Author: {author} | "
                f"Category: {category}"
            )

        return "\n".join(output)

    # Normal search
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

    for book_id, title, author, category, available in results:
        status = "Available" if available else "Not Available"

        output.append(
            f"ID: {book_id} | "
            f"Title: {title} | "
            f"Author: {author} | "
            f"Category: {category} | "
            f"Status: {status}"
        )

    return "\n".join(output)