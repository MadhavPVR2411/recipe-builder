from fastapi import APIRouter, Depends, HTTPException, status

from app.controllers.deps import get_current_user
from app.dto.profile import ProfileResponse, AllergenResponse, DietUpdateRequest
from app.services import profile as service
from app.services.exceptions import AllergenNotFoundException

router = APIRouter(tags=["profile"])


@router.get("/profile", response_model=ProfileResponse)
def get_profile(user: dict = Depends(get_current_user)) -> ProfileResponse:
    return service.get_profile(user["id"])


@router.put("/profile/diet", response_model=ProfileResponse)
def update_diet(body: DietUpdateRequest, user: dict = Depends(get_current_user)) -> ProfileResponse:
    return service.update_diet(user["id"], body.diet_type)


@router.get("/allergens", response_model=list[AllergenResponse])
def list_allergens() -> list[AllergenResponse]:
    return service.list_allergens()


@router.post("/profile/allergens/{allergen_id}", response_model=ProfileResponse)
def add_allergen(allergen_id: int, user: dict = Depends(get_current_user)) -> ProfileResponse:
    try:
        return service.add_allergen(user["id"], allergen_id)
    except AllergenNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allergen not found")


@router.delete("/profile/allergens/{allergen_id}", response_model=ProfileResponse)
def remove_allergen(allergen_id: int, user: dict = Depends(get_current_user)) -> ProfileResponse:
    try:
        return service.remove_allergen(user["id"], allergen_id)
    except AllergenNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Allergen not found")