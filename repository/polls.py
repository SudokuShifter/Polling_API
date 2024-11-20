from collections.abc import Sequence
from datetime import datetime

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from typing import List, Union, Optional

from repository.session_db.session import get_db
from schemas.poll import PollInFirst, PollInChange, QuestionIn, QuestionOut, PollOut
from models.db_models import Poll, Question



class PollRepository:

    @staticmethod
    async def get_all_polls(session: AsyncSession) -> Sequence[Poll]:
        res = await session.scalars(select(Poll))
        if res:
            return [i.to_dict() for i in res.all()]
        raise HTTPException(status_code=404, detail="No polls found")

    @staticmethod
    async def fetch_poll_or_none(poll_id: int, session: AsyncSession) -> Optional[Poll]:
        poll = await session.scalar(select(Poll).where(Poll.id == poll_id))
        return poll

    @staticmethod
    async def get_poll_by_id(poll_id: int, session: AsyncSession) -> Optional[Poll]:
        res = await PollRepository.fetch_poll_or_none(poll_id, session)
        return res

    @staticmethod
    async def polls_by_user(user_id: int, poll_id: int, session: AsyncSession) -> bool:
        res = await PollRepository.fetch_poll_or_none(poll_id, session)
        if res.user_id == user_id:
            return True
        return False

    @staticmethod
    async def poll_is_active(poll_id: int, session: AsyncSession) -> bool:
        poll = await PollRepository.fetch_poll_or_none(poll_id, session)
        if poll.date_end < datetime.now():
            return False
        return True

    @staticmethod
    async def get_questions_by_poll_id(poll_id: int, session: AsyncSession) -> Sequence[Question]:
        res = await session.scalars(select(Question).where(Question.poll_id == poll_id))
        res = res.all()

        if res:
            return res

        raise HTTPException(status_code=404, detail="Poll or Questions not found")

    @staticmethod
    async def create_poll(create_poll: PollInFirst, session: AsyncSession) -> PollOut:
        exist_poll = await session.scalar(select(Poll).where(Poll.title == create_poll.title))

        if exist_poll:
            raise HTTPException(400, detail='Poll already exists')

        new_poll = Poll(**create_poll.dict())
        session.add(new_poll)
        await session.commit()
        await session.refresh(new_poll)
        return PollOut.from_orm(new_poll)

    @staticmethod
    async def update_poll(id_poll: int, upd_poll: PollInChange, session: AsyncSession) -> PollOut:
        poll_in_db = await PollRepository.fetch_poll_or_none(id_poll)
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
        await session.refresh(poll_in_db)
        return PollOut.from_orm(poll_in_db)

    @staticmethod
    async def delete_poll(id_poll: int, session: AsyncSession) -> Optional[dict]:
        poll_in_db = await PollRepository.fetch_poll_or_none(id_poll, session)
        if poll_in_db is None:
            raise HTTPException(404, detail='Poll not found')

        await session.delete(poll_in_db)
        await session.commit()
        return {'message': 'Poll deleted'}

    @staticmethod
    async def add_question_in_poll(id_poll: int, question: QuestionIn, session: AsyncSession) -> QuestionOut:
        poll = await PollRepository.fetch_poll_or_none(id_poll)
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
            await session.refresh(new_question)
            return QuestionOut.from_orm(new_question)
        else:
            raise HTTPException(404, detail='Poll not found')

    @staticmethod
    async def delete_question_in_poll(id_poll: int, id_question: int, session: AsyncSession) -> QuestionOut:
        question = await session.scalar(select(Question).where(
            Question.poll_id == id_poll,
            Question.id == id_question))

        if question:
            await session.delete(question)
            await session.commit()
            await session.refresh(question)
            return QuestionOut.from_orm(question)

        raise HTTPException(status_code=404, detail="Question not found")

