from pydantic import BaseModel, Field, field_validator


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)

    @field_validator("username")
    @classmethod
    def normalise(cls, v: str) -> str:
        v = v.strip().lower()
        if len(v) < 3:
            raise ValueError("username must be at least 3 characters")
        return v

    @field_validator("password")
    @classmethod
    def fits_bcrypt(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password is too long")
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