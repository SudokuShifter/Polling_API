from fastapi import HTTPException

from sqlalchemy.future import select
from db.database import async_session_marker
from passlib.hash import pbkdf2_sha256

from schemas.user import UserIn, UserChange, UserLogin
from models.db_models import User, RoleUserEnum


class UserRepository:

    @staticmethod
    async def get_all_users():
        async with async_session_marker() as session:
            res = await session.execute(select(User))

            return res.scalars().all()


    @staticmethod
    async def login(user: UserLogin):
        async with async_session_marker() as session:
            if user:
                res = await session.execute(select(User).where(User.email == user.email))
                if pbkdf2_sha256.verify(res.password, user.password):
                    return True

            raise HTTPException(401, 'Login or password failed')


    @staticmethod
    async def get_user(user_id: int):
        async with async_session_marker() as session:
            res = await session.execute(select(User).where(User.id == user_id))
            user = res.scalars().first()
            if user:
                return user

            raise HTTPException(404, detail='User not found')




    @staticmethod
    async def create_user(user: UserIn):
        async with async_session_marker() as session:
            new_user = User(username=user.username,
                            email=user.email,
                            password=pbkdf2_sha256(user.password.encode('utf-8')).hexdigest(),
                            role=RoleUserEnum.USER)
            session.add(new_user)

            await session.commit()
            return new_user


    @staticmethod
    async def create_admin_user(user: UserIn):
        async with async_session_marker() as session:
            new_user = User(username=user.username,
                            email=user.email,
                            password=pbkdf2_sha256(user.password.encode('utf-8')).hexdigest(),
                            role=RoleUserEnum.ADMIN)
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


