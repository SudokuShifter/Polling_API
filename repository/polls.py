from ctypes import windll
from os import write

from fastapi import HTTPException

from sqlalchemy.future import select
from db.database import async_session_marker
from schemas import poll

from schemas.poll import PollInFirst, PollInChange
from models.db_models import Poll, Question


class PollRepository:

    @staticmethod
    async def get_all_poll():
        async with async_session_marker() as session:
            res = await session.execute(select(Poll))
            return res.scalars().all()


    @staticmethod
    async def get_poll_by_id(poll_id: int):
        async with async_session_marker() as session:
            res = await session.execute(select(Poll).where(Poll.id == poll_id))
            questions = await session.execute(select(Question).where(Question.id == poll_id))
            return [res.scalars.first(), questions.scalars.all()]


    @staticmethod
    async def create_poll(poll: PollInFirst):
        async with async_session_marker() as session:
            poll = Poll(**poll.dict())
            session.add(poll)
            await session.commit()
            return poll


    @staticmethod
    async def update_poll(id_poll: int, poll: PollInChange):
        async with async_session_marker() as session:
            poll_in_db = await PollRepository.get_poll_by_id(id_poll)
            if poll:
                for key, value in poll.dict(exclude_unset=True).items():
                    setattr(poll_in_db, key, value)
            else:
                raise HTTPException(status_code=404, detail="Poll not found")
            await session.commit()
            return poll


    @staticmethod
    async def delete_poll(id_poll: int):
        async with async_session_marker() as session:
            poll_in_db = await PollRepository.get_poll_by_id(id_poll)
            if poll:
                await session.delete(poll_in_db)
            else:
                raise HTTPException(status_code=404, detail="Poll not found")

            await session.commit()
            return poll

