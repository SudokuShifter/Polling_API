from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from classy_fastapi import Routable, get, post, put, delete

from typing import Optional, Annotated, List

from JWT.JWT_token import JWTToken
from repository.users import UserRepository
from schemas.poll import PollInFirst, PollInChange, PollOut, QuestionIn
from models.db_models import Poll
from repository.polls import PollRepository
from routers.reg_auth import LoginRegister


class PollCrud(APIRouter):

    def __init__(self, model, rep):
        super().__init__()
        self.model = model
        self.rep = rep


    @get('/polls')
    async def get_all_polls(self, response_class = List[PollOut]):
        return JSONResponse(content={'polls': await self.rep.get_all_polls()})


    @get('/polls/{poll_id}')
    async def get_poll(self, poll_id: int, response_class = Optional[PollOut]):
        poll = await self.rep.get_poll(poll_id)
        questions = await self.rep.get_questions_by_poll_id(poll_id)
        return JSONResponse(content={'poll': poll, 'questions': questions})


    @post('/create_poll')
    async def create_poll(self, poll: PollInFirst,
                          current_user: dict = Depends(LoginRegister.get_current_user)):

        if current_user['role'] == 'admin':
            res = await self.model.create_poll(poll)
            return JSONResponse(content={'success_create': res})
        raise HTTPException(status_code=403, detail='Not enough permissions')


    @put('/update_poll/{poll_id}')
    async def update_poll(self, poll_id: int, poll_data: PollInChange,
                          current_user: dict = Depends(LoginRegister.get_current_user)):

        if self.rep.polls_by_user(current_user.get('user'), poll_id):
            if current_user['role'] == 'admin':
                res = await self.rep.update_poll(poll_id, poll_data)
                return JSONResponse(content={'success_delete': res})
            raise HTTPException(status_code=403, detail='Not enough permissions')
        raise HTTPException(status_code=404, detail='Poll not found')


    @delete('/delete_poll/{poll_id}')
    async def delete_poll(self, poll_id: int,
                          current_user: dict = Depends(LoginRegister.get_current_user)):

        if self.rep.polls_by_user(current_user.get('user'), poll_id):
            if current_user['role'] == 'admin':
                res = await self.rep.delete_poll(poll_id)
                return JSONResponse(content={'success_delete': res})
            raise HTTPException(status_code=403, detail='Not enough permissions')
        raise HTTPException(status_code=404, detail='Poll not found')


    @post('/add_question/{poll_id}')
    async def add_question(self, poll_id: int, question: QuestionIn,
                           current_user: dict = Depends(LoginRegister.get_current_user)):
        if question and current_user['role'] == 'admin':
            if UserRepository.polls_by_user(current_user.get('user'), poll_id):
                res = await self.rep.add_question(poll_id, question)
                return JSONResponse(content={'success add question': res})
            raise HTTPException(404, detail='Poll not found')
        raise HTTPException(status_code=401, detail='Not enough permissions')


    @delete('/remove_question/{poll_id}/{question_id}')
    async def remove_question(self, poll_id: int, question_id: int,
                              current_user: dict = Depends(LoginRegister.get_current_user)):

        if current_user['role'] == 'admin':
            if self.rep.polls_by_user(current_user.get('user'), poll_id):
                res = await self.rep.delete_question_in_poll(poll_id, question_id)
                return JSONResponse(content={'success remove question': res})
            raise HTTPException(404, detail='Poll not found')
        raise HTTPException(status_code=401, detail='Not enough permissions')

