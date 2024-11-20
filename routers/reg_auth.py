import jwt
from fastapi import APIRouter, HTTPException, Depends
from classy_fastapi import Routable, get, post
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from typing import Optional, Annotated
import os

from sqlalchemy.ext.asyncio import AsyncSession

from repository.session_db.session import get_db
from routers.JWT.JWT_token import JWTToken
from schemas.user import UserLogin, UserIn
from models.db_models import User
from repository.users import UserRepository


class LoginRegisterRouter:

    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/login')

    def __init__(self, rep):
        self.router = APIRouter()
        self.rep = rep
        self.router.add_api_route('/register', self.register, methods=['POST'])
        self.router.add_api_route('/login', self.login, methods=['POST'])
        self.router.add_api_route('/check_token', self.check_token, methods=['GET'])


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


    async def register(self, user: UserIn, db: AsyncSession = Depends(get_db)):
        if user:
            if user.admin_token and user.admin_token == os.getenv('ADMIN_TOKEN'):
                res = await self.rep.create_user(user, is_admin=True, session=db)
            else:
                res = await self.rep.create_user(user, is_admin=False, session=db)
            return JSONResponse(content={'message': f'Successfully create user {res}'})
        raise HTTPException(status_code=404, detail='Data not found')


    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                    db: AsyncSession = Depends(get_db)):
        res = await self.rep.login(UserLogin(username=form_data.username, password=form_data.password), session=db)
        if res:
            data_to_token = {
                'id': res.id,
                'username': res.username,
                'role': res.role
            }
            return JSONResponse(content={'message': f'Successfully logged in as {res.username}',
                    'token': f'{JWTToken.generate_token(data=data_to_token)}'})
        raise HTTPException(status_code=401, detail='Invalid credentials')


    async def check_token(self, token: str = Depends(OAUTH2_SCHEME)):
        """
        Подключить реддис и из него доставать действующие токены для проверки
        """
        pass




