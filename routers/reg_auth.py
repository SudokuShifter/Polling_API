from fastapi import APIRouter, HTTPException, Depends
from classy_fastapi import Routable, get, post
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from typing import Optional, List, Union, Annotated
import os

from JWT.JWT_token import JWTToken
from schemas.user import UserIn, User, UserOut, UserChange, UserLogin
from schemas.poll import PollOut
from schemas.user_result import UserResult


class LoginRegister(APIRouter):

    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/login')

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
    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        res = await self.rep.login(UserLogin(username=form_data.username, password=form_data.password))
        if res:
            data_to_token = {'username': res.username,
                             'role': res.role}
            return {'message': f'Successfully logged in as {res.username}',
                    'token': f'{JWTToken.generate_token(data_to_token)}'}
        return HTTPException(status_code=401, detail='Invalid credentials')


    @get('/check_token')
    async def check_token(self, token: str = Depends(OAUTH2_SCHEME)):
        """
        Подключить реддис и из него доставать действующие токены для проверки
        """
        pass




