from typing import Optional

from pydantic import BaseModel, Field

from datetime import datetime, timedelta, date


class PollInChange(BaseModel):
    title: str = Field(
        min_length=3, max_length=100
    )
    date_end: date = Field(
        default_factory=lambda: date.today() + timedelta(days=30)
    )

    class Config:
        orm_mode = True


class PollInFirst(PollInChange):
    date_start: datetime.date = Field(
        default_factory=date.today
    )


class PollOut(PollInFirst):
    id: int


class QuestionIn(BaseModel):
    title: str = Field(
        min_length=3, max_length=100
    )
    type: str = Field(
        min_length=1, max_length=100
    )
    answer: Optional[str] = Field(
        min_length=1, max_length=100
    )


class QuestionOut(QuestionIn):
    id: int