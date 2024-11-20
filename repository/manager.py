from repository.polls import PollRepository
from repository.answers import ResultRepository
from repository.users import UserRepository

from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryManager:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db


    @property
    def polls(self) -> PollRepository:
        return PollRepository()

    @property
    def answers(self) -> ResultRepository:
        return ResultRepository()

    @property
    def users(self) -> UserRepository:
        return UserRepository()


