from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from db.database import async_session_marker
from passlib.hash import pbkdf2_sha256
from typing import List, Optional

from schemas.user import UserIn, UserChange, UserLogin, UserOut
from models.db_models import User, RoleUserEnum
from decorators.session import with_session

class UserRepository:


    @staticmethod
    @with_session
    async def get_all_users(session: AsyncSession) -> Sequence[User]:
        res = await session.scalars(select(User))
        return res.all()


    @staticmethod
    @with_session
    async def login(user: UserLogin, session: AsyncSession) -> Optional[User]:
        res = await session.scalar(select(User).where(User.email == user.email))
        if res and pbkdf2_sha256.verify(user.password, res.password):
            return res
        raise HTTPException(401, 'Login failed')


    @staticmethod
    @with_session
    async def get_user(user_id: int, session: AsyncSession) -> Optional[User]:
        user = await session.scalar(select(User).where(User.id == user_id))
        return user if user else None


    @staticmethod
    @with_session
    async def check_unique_email(email: str, session: AsyncSession) -> bool:
        exist_email = await session.scalar(select(User).where(User.email == email))
        return False if exist_email else True


    @staticmethod
    @with_session
    async def create_user(user: UserIn, is_admin: bool, session: AsyncSession) -> Optional[UserOut]:
        if await UserRepository.check_unique_email(user.email, session):
            raise HTTPException(400, 'Email already exists')
        new_user = User(username=user.username,
                        email=user.email,
                        password=pbkdf2_sha256.hash(user.password),
                        role=RoleUserEnum.ADMIN if is_admin else RoleUserEnum.USER)
        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)
        return UserOut.from_orm(new_user)


    @staticmethod
    @with_session
    async def update_user(user_id: int, user: UserChange, session: AsyncSession) -> Optional[UserOut]:
        user_in_db = await UserRepository.get_user(user_id, session)
        if user_in_db:
            for key, value in user.dict(exclude_unset=True).items():
                setattr(user_in_db, key, value)
        else:
            raise HTTPException(404, detail='User not found')

        await session.commit()
        await session.refresh(user_in_db)
        return UserOut.from_orm(user_in_db)


    @staticmethod
    @with_session
    async def delete_user(user_id: int, session: AsyncSession) -> Optional[dict]:
        user_in_db = await UserRepository.get_user(user_id, session)
        if user_in_db:
            await session.delete(user_in_db)
        else:
            raise HTTPException(404, detail='User not found')

        await session.commit()
        return {'message': 'User deleted'}


    @staticmethod
    @with_session
    async def polls_by_user(username: str ,poll_id: int, session: AsyncSession) -> Optional[bool]:
        user_in_db = await session.scalar(select(User).where(User.username == username))
        if user_in_db:
            return poll_id in {poll_id for poll in user_in_db.polls}
        raise HTTPException(404, detail='User not found')
