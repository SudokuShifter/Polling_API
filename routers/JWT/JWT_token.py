from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv
from jwt import ExpiredSignatureError, InvalidTokenError

load_dotenv(dotenv_path='.env')


class JWTToken:

    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    TIME_EXPIRE_TOKEN = 30

    @staticmethod
    def generate_token(data: dict):
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWTToken.TIME_EXPIRE_TOKEN)
        data.update({'exp': expire})
        return jwt.encode(data,JWTToken.SECRET_KEY, algorithm=JWTToken.ALGORITHM)

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, JWTToken.SECRET_KEY, algorithms=[JWTToken.ALGORITHM])
        return payload.get('sub')


