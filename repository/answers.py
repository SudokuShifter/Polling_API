from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from db.database import async_session_marker

from schemas.user_result import UserResultOut
from models.db_models import UserResult, Question
from decorators.session import with_session


class ResultRepository:

    @staticmethod
    @with_session
    async def get_question(question_id: int, session: AsyncSession):
        res = await session.scalar(select(Question).where(Question.id == question_id))
        return res


    @staticmethod
    @with_session
    async def get_all_results(poll_id: int, session: AsyncSession) -> Sequence[UserResultOut]:
        res = await session.scalars(select(UserResult).where(UserResult.poll_id == poll_id))
        return res.all()


    @staticmethod
    @with_session
    async def get_one_result(result_id: int, session: AsyncSession) -> UserResultOut:
        res = await session.scalar(select(UserResult).where(UserResult.id == result_id))
        if not res:
            raise HTTPException(404, detail='result not found')
        return res


    @staticmethod
    @with_session
    async def answer_for_question(answer, question_id, session: AsyncSession) -> bool:
        question = await ResultRepository.get_question(question_id, session)
        if question.current_answer == answer:
            return True
        return False