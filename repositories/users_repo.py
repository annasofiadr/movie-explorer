from database import get_connection


def create_user(username, password_hash):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def get_user_by_username(username):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (username,))

        return cursor.fetchone()

    finally:
        connection.close()


def get_user_by_id(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, username
            FROM users
            WHERE id = ?
        """, (user_id,))

        return cursor.fetchone()

    finally:
        connection.close()