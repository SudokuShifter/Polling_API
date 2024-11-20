from pydantic import BaseModel, Field, ConfigDict


class UserResultOut(BaseModel):
    user_id: int
    poll_id: int
    result: int = Field(
        ge=0
    )

    model_config = ConfigDict(from_attributes=True)


class UserResult(UserResultOut):
    id: int


class AnswerIn(BaseModel):
    answer: str

    model_config = ConfigDict(from_attributes=True)


class AnswerOut(AnswerIn):
    poll_id: int
    user_id: int
    id: int
    point: int
