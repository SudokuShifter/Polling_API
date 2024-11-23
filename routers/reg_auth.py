import jwt
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from classy_fastapi import Routable, get, post
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from typing import Optional, Annotated
import os

from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from repository.session_db.session import get_db
from routers.JWT.JWT_token import JWTToken
from schemas.user import UserLogin, UserIn, UserChange
from models.db_models import User
from repository.users import UserRepository



class LoginRegisterRouter:

    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='user/login')

    def __init__(self, rep):
        self.router = APIRouter()
        self.rep = rep
        self.router.add_api_route('/register',
                                  self.register, methods=['POST'])
        self.router.add_api_route('/login',
                                  self.login, methods=['POST'])
        self.router.add_api_route('/logout',
                                  self.logout, methods=['POST'])
        self.router.add_api_route('/change_data',
                                  self.change_data_user, methods=['PATCH'])
        self.router.add_api_route('/delete_account',
                                  self.delete_account, methods=['DELETE'])


    @staticmethod
    def get_token_from_cookies(request: Request):

        token = request.cookies.get('token')

        if not token:
            raise HTTPException(401, detail='Not authenticated')
        return token



    @staticmethod
    def get_current_user(token: str = Depends(get_token_from_cookies)):
        try:
            print(token)
            payload = JWTToken.decode_token(token)
            user = {'id': payload.get('id'),
                    'user': payload.get('user'),
                    'role': payload.get('role')}
            print(user)
            if user:
                return user

        except ExpiredSignatureError:
                raise ValueError('Token is expired, please login again')
        except InvalidTokenError:
            raise ValueError('Token is invalid, please login again')


    async def register(self, user: UserIn, db: AsyncSession = Depends(get_db)):

        if user:
            if user.admin_token and user.admin_token == os.getenv('ADMIN_TOKEN'):
                res = await self.rep.create_user(user, is_admin=True, session=db)
            else:
                res = await self.rep.create_user(user, is_admin=False, session=db)

            return JSONResponse(content={'message': f'Successfully create user {res}'})

        raise HTTPException(status_code=404, detail='Data not found')


    async def login(self, request: Request, response: Response,
                    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                    db: AsyncSession = Depends(get_db)):

        res = await self.rep.login(UserLogin(username=form_data.username, password=form_data.password), session=db)
        if res:
            data_to_token = {'sub': {
                'id': res.id,
                'username': res.username,
                'role': res.role}
            }
            access_token = JWTToken.generate_token(data=data_to_token)
            response.set_cookie('token', access_token, httponly=True)

            return JSONResponse(content={
                'message': f'Successfully logged in as {res.username}',
                'token': f'{access_token}',
                'cookies': request.cookies},
                                headers=response.headers)

        raise HTTPException(status_code=401, detail='Invalid credentials')


    async def logout(self, response: Response):

        response.set_cookie('token', 'None')
        return JSONResponse(content={'message': 'Successfully logged out'},
                            headers=response.headers)


    async def change_data_user(self,response: Response, new_data: UserChange,
                               db: AsyncSession = Depends(get_db),
                               current_user = Depends(get_current_user)):
        if current_user:
            res = await self.rep.update_user(current_user['id'], new_data, session=db)
            new_data_for_token = {
                'id': current_user['id'],
                'username': new_data.username,
                'role': current_user['role']
            }
            new_token = JWTToken.generate_token(data=new_data_for_token)
            response.set_cookie('token', new_token, httponly=True)
            return JSONResponse(content={'success': True, 'new_data': new_data_for_token}, headers=response.headers)
        raise HTTPException(status_code=403, detail='Not enough permissions')


    async def delete_account(self, db: AsyncSession = Depends(get_db),
                             current_user = Depends(get_current_user)):
        if current_user:
            print(current_user)
            res = await self.rep.delete_user(current_user['id'], session=db)
            return res
        raise HTTPException(status_code=403, detail='Not enough permissions')


    async def check_token(self, token: str = Depends(OAUTH2_SCHEME)):
        """
        Подключить реддис и из него доставать действующие токены для проверки
        """
        pass




