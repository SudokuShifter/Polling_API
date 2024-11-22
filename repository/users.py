from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from db.database import async_session_marker
from passlib.hash import pbkdf2_sha256
from typing import List, Optional

from schemas.user import UserIn, UserChange, UserLogin, UserOut
from models.db_models import User, RoleUserEnum


class UserRepository:

    @staticmethod
    async def get_all_users(session: AsyncSession) -> Sequence[User]:

        res = await session.scalars(select(User))
        return res.all()


    @staticmethod
    async def login(user: UserLogin,
                    session: AsyncSession) -> Optional[User]:

        res = await session.scalar(select(User).where(User.username == user.username))
        if res and pbkdf2_sha256.verify(user.password, res.password):
            return res

        raise HTTPException(401, 'Login failed')


    @staticmethod
    async def get_user(user_id: int, session: AsyncSession) -> Optional[User]:

        user = await session.scalar(select(User).where(User.id == user_id))
        return user if user else None


    @staticmethod
    async def check_unique_email(email: str, session: AsyncSession):

        exist_email = await session.scalar(select(User).where(User.email == email))
        if exist_email:
            return exist_email
        return False


    @staticmethod
    async def create_user(user: UserIn, is_admin: bool, session: AsyncSession):

        if await UserRepository.check_unique_email(user.email, session):
            raise HTTPException(400, 'Email already exists')
        new_user = User(username=user.username,
                        email=user.email,
                        password=pbkdf2_sha256.hash(user.password),
                        role=RoleUserEnum.ADMIN if is_admin else RoleUserEnum.USER)
        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return {'success': {'user': [new_user.username, new_user.email, new_user.role]}}


    @staticmethod
    async def update_user(user_id: int, user: UserChange,
                          session: AsyncSession) -> Optional[dict]:

        user_in_db = await UserRepository.get_user(user_id, session)
        if user_in_db:
            for key, value in user.dict(exclude_unset=True).items():
                setattr(user_in_db, key, value)
        else:
            raise HTTPException(404, detail='User not found')

        await session.commit()
        await session.refresh(user_in_db)

        return {'success': {'user': [user.username, user.email]}}


    @staticmethod
    async def delete_user(user_id: int, session: AsyncSession) -> Optional[dict]:

        user_in_db = await UserRepository.get_user(user_id, session)
        if user_in_db:
            await session.delete(user_in_db)
        else:
            raise HTTPException(404, detail='User not found')

        await session.commit()

        return {'message': 'User deleted'}


    @staticmethod
    async def polls_by_user(user_id: str ,poll_id: int, session: AsyncSession) -> Optional[bool]:

        user_in_db = await session.scalar(select(User).where(User.id == user_id))
        if user_in_db:
            polls = {poll_id for poll_id in user_in_db.polls}
            print(polls)
            return poll_id

        raise HTTPException(404, detail='User not found')
