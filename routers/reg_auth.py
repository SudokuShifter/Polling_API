import jwt
from fastapi import APIRouter, HTTPException, Depends
from classy_fastapi import get, post
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from typing import Optional, Annotated
import os

from routers.JWT.JWT_token import JWTToken
from schemas.user import UserLogin
from models.db_models import User
from repository.users import UserRepository


class LoginRegister(APIRouter):

    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/login')

    def __init__(self, model, rep):
        super().__init__()
        self.model = model
        self.rep = rep


    @staticmethod
    async def get_current_user(token: str = Depends(OAUTH2_SCHEME)):
        try:
            payload = JWTToken.decode_token(token)
            user = {'user': payload.get('user'),
                    'role': payload.get('role')}
            if user:
                return user
            raise HTTPException(401, detail='Invalid Token')
        except HTTPException:
            raise HTTPException(401, detail='Invalid or expired token')


    @post('/register')
    async def register(self, user):
        if user:
            if user.admin_token and user.admin_token == os.getenv('ADMIN_TOKEN'):
                res = await self.rep.create_user(user, is_admin=True)
            else:
                res = await self.rep.create_user(user, is_admin=False)
            return JSONResponse(content={'message': f'Successfully create user {res}'})
        raise HTTPException(status_code=404, detail='Data not found')


    @post('/login')
    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        res = await self.rep.login(UserLogin(username=form_data.username, password=form_data.password))
        if res:
            data_to_token = {
                'id': res.id,
                'username': res.username,
                'role': res.role
            }
            return JSONResponse(content={'message': f'Successfully logged in as {res.username}',
                    'token': f'{JWTToken.generate_token(data_to_token)}'})
        raise HTTPException(status_code=401, detail='Invalid credentials')


    @get('/check_token')
    async def check_token(self, token: str = Depends(OAUTH2_SCHEME)):
        """
        Подключить реддис и из него доставать действующие токены для проверки
        """
        pass




