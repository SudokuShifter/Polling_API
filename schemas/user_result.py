from pydantic import BaseModel, Field

from .poll import PollOut
from .poll import QuestionOut

from typing import List, Optional

from .user import UserOut


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

