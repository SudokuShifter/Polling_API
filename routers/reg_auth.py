from distutils.command.check import check

from fastapi import APIRouter, HTTPException
from classy_fastapi import Routable, get, post

import jwt
from typing import Optional, List, Union
import os
from dotenv import load_dotenv


from schemas.user import UserIn, User, UserOut, UserChange, UserLogin
from schemas.poll import PollOut
from schemas.user_result import UserResult


load_dotenv()


class LoginRegister(APIRouter):


    def __init__(self, model, rep):
        super().__init__()
        self.model = model
        self.rep = rep


    @staticmethod
    def generate_jwt_token():
        pass


    @post('/register')
    async def register(self, user: Optional[UserIn]):
        if user:
            if user.admin_token and user.admin_token == os.getenv('ADMIN_TOKEN'):
                res = await self.rep.create_admin_user(user)
            else:
                res = await self.rep.create_user(user)
            return {'message': f'Successfully create user {res}'}
        raise HTTPException(status_code=404, detail='Data not found')


    @post('/login')
    async def login(self, user: Optional[UserLogin],
                    response_model=Optional[List[Union[UserOut, PollOut, UserResult]]]):
        res = await self.rep.login(user)
        if res:
            pass




