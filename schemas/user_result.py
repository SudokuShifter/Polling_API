from pydantic import BaseModel, Field


class UserResultOut(BaseModel):
    result: int = Field(
        ge=0
    )
    poll_id: int
    user_id: int

    class Config:
        orm_mode = True


class UserResult(UserResultOut):
    id: int

