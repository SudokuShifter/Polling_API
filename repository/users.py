from fastapi import HTTPException

from sqlalchemy.future import select
from db.database import async_session_marker

from schemas.user import UserIn, UserChange
from models.db_models import User


class UserRepository:

    @staticmethod
    async def get_all_users():
        async with async_session_marker() as session:
            res = await session.execute(select(User))
            return res.scalars().all()


    @staticmethod
    async def get_user(user_id: int):
        async with async_session_marker() as session:
            res = await session.execute(select(User).where(User.id == user_id))
            user = res.scalars().first()
            if not user:
                raise HTTPException(404, detail='User not found')
            return user


    @staticmethod
    async def create_user(user: UserIn):
        async with async_session_marker() as session:
            new_user = User(**user.dict())
            session.add(new_user)
            await session.commit()
            return new_user


    @staticmethod
    async def update_user(user_id: int, user: UserChange):
        async with async_session_marker() as session:
            user_in_db = await UserRepository.get_user(user_id)
            if user_in_db:
                for key, value in user.dict(exclude_unset=True).items():
                    setattr(user_in_db, key, value)
            else:
                raise HTTPException(404, detail='User not found')

            await session.commit()
            return user


    @staticmethod
    async def delete_user(user_id: int):
        async with async_session_marker() as session:
            user_in_db = await UserRepository.get_user(user_id)
            if user_in_db:
                await session.delete(user_in_db)
            else:
                raise HTTPException(404, detail='User not found')

            await session.commit()
            return {'message': 'User deleted'}


