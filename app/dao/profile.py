from app.dao.db import get_session
from app.models import Allergen, User, UserProfile


def _to_dict(user: User, profile: UserProfile) -> dict:
    return {
        "diet_type": profile.diet_type,
        "allergens": [{"id": a.id, "name": a.name} for a in user.allergens],
    }


def get_profile(user_id: int) -> dict:
    with get_session() as session:
        user = session.get(User, user_id)
        profile = session.get(UserProfile, user_id)
        return _to_dict(user, profile)


def update_diet(user_id: int, diet_type: str) -> dict:
    with get_session() as session:
        user = session.get(User, user_id)
        profile = session.get(UserProfile, user_id)
        profile.diet_type = diet_type
        return _to_dict(user, profile)


def add_allergen(user_id: int, allergen_id: int) -> dict:
    with get_session() as session:
        user = session.get(User, user_id)
        profile = session.get(UserProfile, user_id)
        allergen = session.get(Allergen, allergen_id)
        if allergen not in user.allergens:
            user.allergens.append(allergen)
        return _to_dict(user, profile)


def remove_allergen(user_id: int, allergen_id: int) -> dict:
    with get_session() as session:
        user = session.get(User, user_id)
        profile = session.get(UserProfile, user_id)
        allergen = session.get(Allergen, allergen_id)
        if allergen in user.allergens:
            user.allergens.remove(allergen)
        return _to_dict(user, profile)
