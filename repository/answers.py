from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from db.database import async_session_marker

from schemas.user_result import UserResultOut
from models.db_models import UserResult
from decorators.session import with_session


class ResultRepository:

    @staticmethod
    @with_session
    async def get_all_results(session: AsyncSession) -> Sequence[UserResultOut]:
        res = await session.scalars(select(UserResult))
        return res.all()


    @staticmethod
    @with_session
    async def get_one_result(result_id: int, session: AsyncSession) -> UserResultOut:
        res = await session.scalar(select(UserResult).where(UserResult.id == result_id))
        if not res:
            raise HTTPException(404, detail='result not found')
        return res
