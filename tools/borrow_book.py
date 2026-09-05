from langchain_core.tools import tool
import sqlite3

DB_NAME = "library.db"


@tool
def borrow_book(book_title: str) -> str:
    """Borrow an available book from the library."""

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

    if not available:
        conn.close()
        return f"'{title}' is currently borrowed and cannot be borrowed."

    cursor.execute("""
        UPDATE books
        SET available = 0
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    return f"Successfully borrowed '{title}'."