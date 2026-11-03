from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Credentials(BaseModel):
    """Shared fields and username cleanup for signup and login."""
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)

    @field_validator("username")
    @classmethod
    def normalise(cls, v: str) -> str:
        v = v.strip().lower()
        if len(v) < 3:
            raise ValueError("username must be at least 3 characters")
        return v


class SignupRequest(Credentials):
    pass


class LoginRequest(Credentials):
    pass


class UserResponse(BaseModel):
    id: int
    username: str
    diet_type: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"