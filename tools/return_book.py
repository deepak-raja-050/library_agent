from langchain_core.tools import tool
import sqlite3

DB_NAME = "library.db"


@tool
def return_book(book_title: str) -> str:
    """Return a borrowed book to the library."""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, available
        FROM books
        WHERE title LIKE ?
    """, (f"%{book_title}%",))

    book = cursor.fetchone()

    if not book:
        conn.close()
        return f"Book '{book_title}' was not found in the library."

    book_id, title, available = book

    if available:
        conn.close()
        return f"'{title}' is already marked as available."

    cursor.execute("""
        UPDATE books
        SET available = 1
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    return f"Successfully returned '{title}'."