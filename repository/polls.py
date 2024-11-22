from collections.abc import Sequence
from datetime import datetime

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from typing import Optional, Union, List

from starlette.responses import JSONResponse

from schemas.poll import PollInFirst, PollInChange, QuestionIn, QuestionOut, PollOut
from models.db_models import Poll, Question



class PollRepository:

    @staticmethod
    def generate_response(status_code: int, detail: str):

        return JSONResponse(status_code=status_code, content=detail)


    @staticmethod
    async def get_all_polls(session: AsyncSession) -> Union[dict, JSONResponse]:

        res = await session.scalars(select(Poll))
        res = res.all()
        return {'polls': [poll.title for poll in res]}


    @staticmethod
    async def fetch_poll_or_none(poll_id: int,
                                 session: AsyncSession) -> Union[Poll, JSONResponse]:

        res = await session.scalar(select(Poll).where(Poll.id == poll_id))
        return res



    @staticmethod
    async def get_poll_by_id(poll_id: int, session: AsyncSession) -> dict[str: int | str]:

        res = await PollRepository.fetch_poll_or_none(poll_id, session)
        if res:
            return {'poll': [f'Poll_title - {res.title}', f'Poll_id - {res.id}']}


    @staticmethod
    async def polls_by_user(user_id: int, poll_id: int,
                            session: AsyncSession) -> bool:

        res = await PollRepository.fetch_poll_or_none(poll_id, session)
        if res.user_id == user_id:
            return True
        return False


    @staticmethod
    async def poll_is_active(poll_id: int,
                             session: AsyncSession) -> Union[bool, JSONResponse]:

        poll = await PollRepository.fetch_poll_or_none(poll_id, session)
        if poll is None:
            return PollRepository.generate_response(404, 'poll not found')
        if poll.date_end < datetime.now().date():
            return False

        return True


    @staticmethod
    async def get_questions_by_poll_id(poll_id: int,
                                       session: AsyncSession) -> dict[str: List[str]]:

        res = await session.scalars(select(Question).where(Question.poll_id == poll_id))
        questions = res.all()
        return {'questions': [quest.title for quest in questions]}



    @staticmethod
    async def create_poll(user_id: int, create_poll: PollInFirst,
                          session: AsyncSession) -> dict[str:bool]:

        exist_poll = await session.scalar(select(Poll).where(Poll.title == create_poll.title))

        if exist_poll:
            raise HTTPException(400, detail='Poll already exists')

        if create_poll.date_end < datetime.now().date() or create_poll.date_end < create_poll.date_start:
            raise HTTPException(400, detail='Poll start date is invalid')

        new_poll = Poll(**create_poll.dict())
        new_poll.user_id = user_id
        session.add(new_poll)
        await session.commit()

        return {'success': True}


    @staticmethod
    async def update_poll(id_poll: int, upd_poll: PollInChange,
                          session: AsyncSession) -> dict[str:bool]:

        poll_in_db = await PollRepository.fetch_poll_or_none(id_poll, session)
        exist_polls = await session.scalar(select(Poll).where(
            Poll.title == upd_poll.title,
            Poll.id != id_poll))

        if exist_polls:
            raise HTTPException(400, detail='Poll already exists')

        if poll_in_db is None:
            raise HTTPException(404, detail='Poll not found')

        for key, value in upd_poll.dict(exclude_unset=True).items():
            setattr(poll_in_db, key, value)

        await session.commit()

        return {'success': True}


    @staticmethod
    async def delete_poll(id_poll: int,
                          session: AsyncSession) -> dict[str:bool]:

        poll_in_db = await PollRepository.fetch_poll_or_none(id_poll, session)
        if poll_in_db is None:
            raise HTTPException(404, detail='Poll not found')

        await session.delete(poll_in_db)
        await session.commit()

        return {'success': True}


    @staticmethod
    async def add_question_in_poll(id_poll: int, question: QuestionIn,
                                   session: AsyncSession) -> dict[str:bool]:

        poll = await PollRepository.fetch_poll_or_none(id_poll, session)
        exist_question = await session.scalar(select(Question).where(
            Question.poll_id == id_poll,
            Question.title == question.title))

        if exist_question:
            raise HTTPException(400, detail='Question already exists')

        if poll:
            new_question = Question(**question.dict())
            new_question.poll_id = id_poll
            session.add(new_question)
            await session.commit()
            return {'success': True}
        else:
            raise HTTPException(404, detail='Poll not found')


    @staticmethod
    async def delete_question_in_poll(poll_id: int, id_question: int,
                                      session: AsyncSession) -> dict[str:bool]:

        question = await session.scalar(select(Question).where(
            Question.id == id_question,
            Question.poll_id == poll_id))

        if question:
            await session.delete(question)
            await session.commit()
            return {'success': True}

        raise HTTPException(status_code=404, detail="Question not found")

