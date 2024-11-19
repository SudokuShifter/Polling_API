from pydantic import BaseModel, Field


class UserResultOut(BaseModel):
    user_id: int
    poll_id: int
    result: int = Field(
        ge=0
    )

    class Config:
        orm_mode = True


class UserResult(UserResultOut):
    id: int


class AnswerIn(BaseModel):
    poll_id: int
    user_id: int
    answer: str

    class Config:
        orm_mode = True


class AnswerOut(AnswerIn):
    id: int