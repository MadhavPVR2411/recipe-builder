from app.dao import allergen as allergen_dao
from app.dao import profile as profile_dao
from app.dto.profile import AllergenResponse, ProfileResponse
from app.services.exceptions import AllergenNotFoundException


def get_profile(user_id: int) -> ProfileResponse:
    return ProfileResponse(**profile_dao.get_profile(user_id))


def update_diet(user_id: int, diet_type: str) -> ProfileResponse:
    return ProfileResponse(**profile_dao.update_diet(user_id, diet_type))


def list_allergens() -> list[AllergenResponse]:
    return [AllergenResponse(**a) for a in allergen_dao.list_all()]


def add_allergen(user_id: int, allergen_id: int) -> ProfileResponse:
    if allergen_dao.find_by_id(allergen_id) is None:
        raise AllergenNotFoundException(allergen_id)
    return ProfileResponse(**profile_dao.add_allergen(user_id, allergen_id))


def remove_allergen(user_id: int, allergen_id: int) -> ProfileResponse:
    if allergen_dao.find_by_id(allergen_id) is None:
        raise AllergenNotFoundException(allergen_id)
    return ProfileResponse(**profile_dao.remove_allergen(user_id, allergen_id))
