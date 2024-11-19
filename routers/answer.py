from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from classy_fastapi import get, post

from schemas.user_result import AnswerIn
from routers.reg_auth import LoginRegister
from repository.polls import PollRepository


class Answer(APIRouter):

    def __init__(self, model, rep):
        super().__init__()
        self.model = model
        self.rep = rep


    @staticmethod
    async def is_user(current_user: dict) -> bool:
        if current_user['role'] == 'user':
            return True
        raise HTTPException(status_code=403, detail='Not permission')


    @get('/my_results')
    async def get_my_results(self, current_user: dict = Depends(LoginRegister.get_current_user)):
        await self.is_user(current_user)
        user_id = current_user['id']
        results = await self.rep.get_all_results(user_id=user_id)
