from datetime import UTC, datetime

from sqlalchemy import select

from app.dao.db import get_session
from app.models import User, UserProfile


def find_by_username(username: str) -> dict | None:
    with get_session() as session:
        user = session.scalar(select(User).where(User.username == username))
        if user is None:
            return None
        return {
            "id": user.id,
            "username": user.username,
            "password_hash": user.password_hash,
        }


def find_by_id(user_id: int) -> dict | None:
    with get_session() as session:
        user = session.get(User, user_id)
        if user is None:
            return None
        return {"id": user.id, "username": user.username}


def create_user(username: str, password_hash: str) -> dict:
    with get_session() as session:
        user = User(username=username, password_hash=password_hash)
        session.add(user)
        session.flush()  # need user.id for the profile
        profile = UserProfile(user_id=user.id)
        session.add(profile)
        session.flush()
        session.refresh(profile)
        return {
            "id": user.id,
            "username": user.username,
            "diet_type": profile.diet_type,
        }


def touch_last_login(user_id: int) -> dict:
    with get_session() as session:
        profile = session.get(UserProfile, user_id)
        profile.last_login_at = datetime.now(UTC)
        return {"diet_type": profile.diet_type, "last_login_at": profile.last_login_at}
