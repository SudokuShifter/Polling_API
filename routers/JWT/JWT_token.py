from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='.env')


class JWTToken:

    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    TIME_EXPIRE_TOKEN = 30

    @staticmethod
    def generate_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWTToken.TIME_EXPIRE_TOKEN)
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode,JWTToken.SECRET_KEY, algorithm=JWTToken.ALGORITHM)

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, JWTToken.SECRET_KEY, algorithms=[JWTToken.ALGORITHM])
        return payload.get('sub')


