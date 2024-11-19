from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import async_session_marker
from fastapi import HTTPException


def with_session(func):
    """
    Декоратор для управления сессиями в репозиториях
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session_marker() as session:
            try:
                return await func(*args, **kwargs)
            except Exception:
                raise
            except Exception as ex:
                await session.rollback()
                raise ex
        return wrapper