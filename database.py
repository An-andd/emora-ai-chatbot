import sqlite3

# Database connection
conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    title TEXT,
    user_message TEXT,
    emotion TEXT,
    confidence REAL,
    bot_response TEXT
)
""")

conn.commit()


def save_chat(session_id, user_message, emotion, confidence, bot_response):

    # Check if this session already has a title
    cursor.execute(
        "SELECT title FROM chats WHERE session_id=? LIMIT 1",
        (session_id,)
    )

    row = cursor.fetchone()

    if row is None:
        # Generate automatic chat title
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM chats")
        count = cursor.fetchone()[0] + 1

        title = f"Chat {count}"

    else:
        title = row[0]

    # Insert message
    cursor.execute("""
        INSERT INTO chats
        (session_id, title, user_message, emotion, confidence, bot_response)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, title, user_message, emotion, confidence, bot_response))

    conn.commit()