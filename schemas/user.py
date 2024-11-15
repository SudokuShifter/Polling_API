from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserOut(BaseModel):
    username: str = Field(
        min_length=3, max_length=50
    )
    email: EmailStr = Field(
        min_length=3, max_length=50
    )

    class Config:
        orm_mode = True


class UserIn(UserOut):
    password: str = Field(
        min_length=8, max_length=50
    )
    admin_token: Optional[str] = Field(
        default=None, min_length=3, max_length=50
    )


class User(UserIn):
    id: int
    role: str = Field(min_length=3, max_length=50, default='user')


