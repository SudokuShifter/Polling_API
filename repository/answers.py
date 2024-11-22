from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from starlette.responses import JSONResponse

from db.database import async_session_marker
from routers.answer import AnswerRouter
from schemas.poll import QuestionIn
from schemas.user import UserIn

from schemas.user_result import UserResult as UserRes
from models.db_models import UserResult, Question, Answer



class ResultRepository:

    @staticmethod
    async def get_question(question_id: int,
                           session: AsyncSession) -> Question:

        res = await session.scalar(select(Question).where(Question.id == question_id))
        print(res)
        if not res:
            raise HTTPException(404, detail="Question not found")
        return res


    @staticmethod
    async def get_all_results_by_poll_id(poll_id: int,
                                         session: AsyncSession) -> Sequence[UserRes]:

        res = await session.scalars(select(UserResult).where(UserResult.poll_id == poll_id))

        return res.all()


    @staticmethod
    async def get_all_results_by_user_id(user_id: int,
                                         session: AsyncSession) -> Sequence[UserRes]:

        res = await session.scalars(select(UserResult).where(UserResult.user_id == user_id))

        return res.all()


    @staticmethod
    async def get_one_result(result_id: int,
                             session: AsyncSession) -> UserRes:

        res = await session.scalar(select(UserResult).where(UserResult.id == result_id))
        if not res:
            raise HTTPException(404, detail='result not found')

        return res



    @staticmethod
    async def answer_for_question(answer, question_id,
                                  session: AsyncSession) -> bool:

        question = await ResultRepository.get_question(question_id, session)
        if question.current_answer == answer:
            return True

        return False


    @staticmethod
    async def add_result_for_question(point: bool, answer: str,
                                      question: QuestionIn, user_id: int,
                                      session: AsyncSession) -> dict:

        answer_for_1_question = Answer(
            user_id=user_id if user_id else None,
            answer=answer,
            point=point,
            question_id=question.id,
            poll_id=question.poll_id
        )

        exist_answer = await session.scalar(select(Answer).where(
            Answer.user_id == user_id,
            Answer.question_id == question.id))

        if exist_answer:
            raise HTTPException(409, detail='answer already exists')

        session.add(answer_for_1_question)
        await session.commit()

        return {'Success': 'Answer is save'}


    @staticmethod
    async def generate_result(poll_id: int, user_id: int,
                              session: AsyncSession) -> dict:

        res = await session.scalars(select(Answer).where(
            Answer.user_id == user_id,
            Answer.poll_id == poll_id))

        answers = res.all()
        user_res = UserResult(user_id=user_id,
                              poll_id=poll_id,
                              result=[i.point for i in res].count(True))
        session.add(user_res)
        await session.commit()

        return {'Success': 'Result is save', 'id_poll': poll_id, 'your_res': user_res.result}

