from repository.polls import PollRepository
from repository.answers import ResultRepository
from repository.users import UserRepository


class RepositoryManager:

    @property
    def polls(self) -> PollRepository:
        return PollRepository()

    @property
    def answers(self) -> ResultRepository:
        return ResultRepository()

    @property
    def users(self) -> UserRepository:
        return UserRepository()


