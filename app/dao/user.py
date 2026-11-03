from app.dao.db import get_cursor


def find_by_username(username: str) -> dict | None:
    with get_cursor() as cur:
        cur.execute(
            'SELECT id, username, password_hash FROM "user" WHERE username = %s', (username,)
        )
        return cur.fetchone()

def find_by_id(user_id: int) -> dict | None:
    with get_cursor() as cur:
        cur.execute('SELECT id, username, FROM "user" WHERE user_id = %s', (user_id,))
        return cur.fetchone()

def create_user(username: str, password_hash:str) -> dict:
    with get_cursor() as cur:
        cur.execute(
            'INSERT INTO "user" (username, password_hash) VALUES (%s, %s) RETURNING id, username',
            (username,password_hash),
        )
        user = cur.fetchone()
        cur.execute(
            "INSERT INTO user_profile (user_id) VALUES (%s) RETURNING diet_type", (user["id"],))

        profile = cur.fetchone()
        return {**user, "diet_type": profile["diet_type"]}


def touch_last_login(user_id: int) -> dict:
    with get_cursor() as cur:
        cur.execute(
            "UPDATE user_profile SET last_login_at = now() WHERE user_id = %s "
            "RETURNING diet_type, last_login_at",
            (user_id,),
        )
        return cur.fetchone()
