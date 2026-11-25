from fastapi import APIRouter, Depends, Query

from app.controllers.deps import get_current_user
from app.dto.recipe import SuggestionsResponse
from app.services import suggestion as suggestion_service

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


@router.get("", response_model=SuggestionsResponse)
def get_suggestions(
    cuisine: str | None = None,
    max_time: int | None = Query(default=None, gt=0),
    user: dict = Depends(get_current_user),
) -> SuggestionsResponse:
    return suggestion_service.get_suggestions(user["id"], cuisine, max_time)
