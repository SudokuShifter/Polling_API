from fastapi import HTTPException

from sqlalchemy.future import select
from db.database import async_session_marker

from schemas.user_result import UserResultOut
from models.db_models import UserResult


class ResultRepository:

    @staticmethod
    async def get_all_results():
        async with async_session_marker() as session:
            res = await session.execute(select(UserResult))
            return res.scalars.all()


    @staticmethod
    async def get_one_result(result_id):
        async with async_session_marker() as session:
            res = await session.execute(select(UserResult).where(UserResult.id == result_id))
            res = res.scalars.first()
            if not res:
                raise HTTPException(404, detail='result not found')
            return res
