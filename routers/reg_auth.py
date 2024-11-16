from distutils.command.check import check

from fastapi import APIRouter, HTTPException

import jwt
from typing import Optional
import os
from dotenv import load_dotenv


from schemas.user import UserIn, User, UserOut
from models.db_models import User


reg_auth = APIRouter()
load_dotenv()


@reg_auth.post('/register')
async def register(user: Optional[UserIn]):
    if user:
        user_data = user.dict()
        if user_data['admin_token'] and user_data['admin_token'] == os.getenv('ADMIN_TOKEN'):
            pass




@reg_auth.get('/login')
async def login():
    pass