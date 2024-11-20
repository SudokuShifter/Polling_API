from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from starlette.responses import JSONResponse

from db.database import async_session_marker
from routers.answer import Answer
from schemas.poll import QuestionIn
from schemas.user import UserIn

from schemas.user_result import UserResult as UserRes
from models.db_models import UserResult, Question, Answer
from decorators.session import with_session


class ResultRepository:

    @staticmethod
    @with_session
    async def get_question(question_id: int, session: AsyncSession):
        res = await session.scalar(select(Question).where(Question.id == question_id))
        if not res:
            raise HTTPException(404, detail="Question not found")
        return res


    @staticmethod
    @with_session
    async def get_all_results_by_poll_id(poll_id: int, session: AsyncSession) -> Sequence[UserRes]:
        res = await session.scalars(select(UserResult).where(UserResult.poll_id == poll_id))
        return res.all()


    @staticmethod
    @with_session
    async def get_all_results_by_user_id(user_id: int, session: AsyncSession) -> Sequence[UserRes]:
        res = await session.scalars(select(UserResult).where(UserResult.user_id == user_id))
        return res.all()


    @staticmethod
    @with_session
    async def get_one_result(result_id: int, session: AsyncSession) -> UserRes:
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


    @staticmethod
    @with_session
    async def add_result_for_question(point: bool, answer: str,
                                      question: QuestionIn, user_id: int, session: AsyncSession) -> JSONResponse:

        answer_for_1_question = Answer(
            user_id=user_id if user_id else None,
            answer=answer,
            point=point,
            question_id=question.id,
            poll_id=question.poll_id
        )

        exist_answer = await session.scalar(select(Answer()).where(
            Answer.user_id == user_id,
            Answer.question_id == question.id))

        if exist_answer:
            raise HTTPException(409, detail='answer already exists')

        session.add(answer_for_1_question)
        await session.commit()
        return JSONResponse({'Success': 'Answer is save'})


    @staticmethod
    @with_session
    async def generate_result(questions: Sequence[Question],
                                                        user_id: int, session: AsyncSession) -> UserRes:
        try:
            results = [i.answers.point for i in questions if i.answers.user_id == user_id]
            points = len([i for i in results if i])
            result = UserResult(
                user_id=user_id,
                poll_id=questions[0].poll_id,
                result=points,
            )
            exist_result = await session.scalar(select(UserResult).where(
                UserResult.user_id == user_id,
                UserResult.poll_id == questions[0].poll_id))
            session.add(result)
            await session.commit()
            await session.refresh(result)
            return result
        except HTTPException:
            raise HTTPException(404, detail='Question or detail not found')