import sqlite3

DB_NAME = "library.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            available INTEGER DEFAULT 1
        )
    """)

    # Add sample books only if database is empty
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]

    if count == 0:
        books = [
            ("Python Crash Course", "Eric Matthes", "Programming", 1),
            ("Automate the Boring Stuff with Python", "Al Sweigart", "Programming", 1),
            ("Clean Code", "Robert C. Martin", "Programming", 0),
            ("Artificial Intelligence: A Modern Approach", "Stuart Russell", "AI", 1),
            ("Hands-On Machine Learning", "Aurélien Géron", "Machine Learning", 1),
            ("The Pragmatic Programmer", "Andrew Hunt", "Programming", 1),
            ("Deep Learning", "Ian Goodfellow", "AI", 0),
            ("Introduction to Algorithms", "Thomas H. Cormen", "Computer Science", 1)
        ]

        cursor.executemany("""
            INSERT INTO books (title, author, category, available)
            VALUES (?, ?, ?, ?)
        """, books)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Library database created successfully.")