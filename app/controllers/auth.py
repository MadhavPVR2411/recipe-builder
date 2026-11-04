from fastapi import APIRouter, HTTPException, status
from app.services import auth as service
from app.dto.auth import LoginRequest, TokenResponse,SignupRequest,UserResponse
from app.services.exceptions import InvalidCredentialsException, UsernameAlreadyExistsException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(body:SignupRequest) -> UserResponse:
    try:
        return service.signup(body.username, body.password)
    except UsernameAlreadyExistsException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest) -> TokenResponse:
    try:
        return service.login(body.username, body.password)
    except InvalidCredentialsException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
