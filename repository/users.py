from http.client import responses

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from db.database import async_session_marker

from schemas.user import UserIn, UserChange
from models.db_models import User


class UserRepository:

    user_model = User

    @staticmethod
    async def get_all_users():
        async with async_session_marker() as session:
            res = await session.execute(select(User))
            return res.scalars().all()


    @staticmethod
    async def get_user(user_id: int):
        async with async_session_marker() as session:
            res = await session.execute(select(User).where(User.id == user_id))
            return res.scalars().first()


    @staticmethod
    async def create_user(user: UserIn):
        async with async_session_marker() as session:
            async with session.begin():
                new_user = User(**user.dict())
                session.add(new_user)
            await session.commit()
            return new_user


    @staticmethod
    async def update_user(user_id: int, user: UserChange):
        async with async_session_marker() as session:
            async with session.begin():
                user_in_db = await session.execute(select(User).where(User.id == user_id))
                user_in_db = user_in_db.scalar().first()

                if not user:
                    for key, value in user.dict(exclude_unset=True).items():
                        setattr(user_in_db, key, value)

            await session.commit()
            return user

    @staticmethod
    async def delete_user(user_id: int):
        async with async_session_marker() as session:
            async with session.begin():
                user_in_db = await session.execute(select(User).where(User.id == user_id))
                if user_in_db.scalars().first():
                    await session.delete(user_in_db)
            await session.commit()
            return user_in_db


