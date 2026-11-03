from app.db import get_cursor


def find_by_username(username: str) -> dict | None:
    with get_cursor() as cur:
        cur.execute(
            'SELECT id, username FROM "user" WHERE username = %s', (username,)
        )
        return cur.fetchone()


def create_user(username: str) -> dict:
    """Insert the user and its default profile in one transaction."""
    with get_cursor() as cur:
        cur.execute(
            'INSERT INTO "user" (username) VALUES (%s) RETURNING id, username',
            (username,),
        )
        user = cur.fetchone()
        cur.execute("INSERT INTO user_profile (user_id) VALUES (%s)", (user["id"],))
        return user


def touch_last_login(user_id: int) -> dict:
    with get_cursor() as cur:
        cur.execute(
            "UPDATE user_profile SET last_login_at = now() WHERE user_id = %s "
            "RETURNING diet_type, last_login_at",
            (user_id,),
        )
        return cur.fetchone()
