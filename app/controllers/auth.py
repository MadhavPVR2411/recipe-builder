from fastapi import APIRouter

from app.services import auth as service
from app.dto.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest) -> LoginResponse:
    return service.login(body.username)

