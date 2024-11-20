from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import async_session_marker
from fastapi import HTTPException


async def get_db() -> AsyncSession:
    async with async_session_marker() as session:
        yield session
