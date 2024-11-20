from typing import Optional, List

from pydantic import BaseModel, Field

from datetime import datetime, timedelta, date


class QuestionIn(BaseModel):
    title: str = Field(
        min_length=3, max_length=100
    )
    type: str = Field(
        min_length=1, max_length=100
    )
    current_answer: Optional[str] = Field(
        min_length=1, max_length=100
    )

    class Config:
        orm_mode = True


class QuestionOut(QuestionIn):
    id: int
    poll_id: Optional[int]


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
    questions: Optional[List[QuestionOut] | None]