from http.client import responses

from sqlalchemy.orm import Session
from db.database import async_session_marker
from models.db_models import User


class UserRepository:

    user_model = User

    @classmethod
    async def get_all_users(cls):
        res = await cls.session.query(User).all()
        return res




