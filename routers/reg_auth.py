from fastapi import APIRouter
from schemas.user import UserIn, User, UserOut
from models.db_models import User
import jwt


reg_auth = APIRouter()


@reg_auth.post('/register')
async def register(user_in: UserIn):


@reg_auth.get('/login')
async def login():
    pass