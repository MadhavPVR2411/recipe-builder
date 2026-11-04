from app.dao import user as dao
from app.services.exceptions import UsernameAlreadyExistsException, InvalidCredentialsException
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core import config
from app.dto.auth import UserResponse,TokenResponse

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
def create_access_token(user_id:int)-> str:
    expires_delta = timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
def signup(username:str, password:str) -> UserResponse:
    if dao.find_by_username(username) is not None:
        raise UsernameAlreadyExistsException(username)
    user = dao.create_user(username, hash_password(password))
    return UserResponse(**user)
def login(username:str, password:str) -> TokenResponse:
    user = dao.find_by_username(username)
    if user is None or not verify_password(password,user["password_hash"]):
        raise InvalidCredentialsException()
    dao.touch_last_login(user["id"])
    return TokenResponse(access_token=create_access_token(user["id"]))