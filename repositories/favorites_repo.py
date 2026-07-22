from database import get_connection


# CREATE
def add_favorite(user_id, movie):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO favorites (
                user_id,
                movie_id,
                title,
                poster_path,
                rating
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            movie["id"],
            movie["title"],
            movie.get("poster_path"),
            movie.get("vote_average")
        ))

        connection.commit()

    finally:
        connection.close()


# READ ALL
def get_all_favorites(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM favorites
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))

        return cursor.fetchall()

    finally:
        connection.close()


# READ ONE
def get_favorite(user_id, movie_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM favorites
            WHERE user_id = ?
              AND movie_id = ?
        """, (user_id, movie_id))

        return cursor.fetchone()

    finally:
        connection.close()


def is_favorite(user_id, movie_id):
    return get_favorite(user_id, movie_id) is not None


# UPDATE
def update_favorite(user_id, movie):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE favorites
            SET title = ?,
                poster_path = ?,
                rating = ?
            WHERE user_id = ?
              AND movie_id = ?
        """, (
            movie["title"],
            movie.get("poster_path"),
            movie.get("vote_average"),
            user_id,
            movie["id"]
        ))

        connection.commit()

    finally:
        connection.close()


# DELETE
def delete_favorite(user_id, movie_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM favorites
            WHERE user_id = ?
              AND movie_id = ?
        """, (user_id, movie_id))

        connection.commit()

    finally:
        connection.close()