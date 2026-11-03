from app.dao import user as dao
from app.dto.auth import LoginResponse


def login(username: str) -> LoginResponse:
    user = dao.find_by_username(username)
    created = user is None
    if created:
        user = dao.create_user(username)
    profile = dao.touch_last_login(user["id"])
    return LoginResponse(
        id=user["id"],
        username=user["username"],
        diet_type=profile["diet_type"],
        last_login_at=profile["last_login_at"],
        created=created,
    )
