from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)

    @field_validator("username")
    @classmethod
    def normalise(cls, v: str) -> str:
        v = v.strip().lower()
        if len(v) < 3:
            raise ValueError("username must be at least 3 characters")
        return v


class LoginResponse(BaseModel):
    id: int
    username: str
    diet_type: str
    last_login_at: datetime
    created: bool
