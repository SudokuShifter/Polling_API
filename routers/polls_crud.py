from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from classy_fastapi import Routable, get, post, put, delete

from typing import Optional, Annotated, List


from routers.reg_auth import LoginRegister


class PollCrud(APIRouter):

    def __init__(self, model, rep):
        super().__init__()
        self.model = model
        self.rep = rep

    @staticmethod
    async def is_admin(current_user: dict) -> bool:
        if current_user['role'] == 'admin':
            return True
        raise HTTPException(status_code=403, detail='Not permissions')


    async def user_has_poll_access(self, current_user: dict, poll_id: int) -> bool:
        if not await self.rep.polls_by_user(current_user['username'], poll_id):
            raise HTTPException(status_code=404, detail='Poll not found')
        return True


    @staticmethod
    def generate_response(success: bool, data=None, detail=None) -> JSONResponse:
        return JSONResponse(content={'success': success, 'data': data, 'detail': detail})


    @get('/polls')
    async def get_all_polls(self):
        res = await self.rep.get_all_polls()
        return PollCrud.generate_response(success=True, data={'polls': res})


    @get('/polls/{poll_id}')
    async def get_poll(self, poll_id: int):
        poll = await self.rep.get_poll(poll_id)
        questions_full = await self.rep.get_questions_by_poll_id(poll_id)
        questions = [question.title for question in questions_full]
        return PollCrud.generate_response(success=True, data={'poll': poll, 'questions': questions})


    @post('/create_poll')
    async def create_poll(self, poll,
                          current_user: dict = Depends(LoginRegister.get_current_user)):

        await self.is_admin(current_user)
        res = await self.model.create_poll(poll)
        return PollCrud.generate_response(success=True, data={'success_create': res})



    @put('/update_poll/{poll_id}')
    async def update_poll(self, poll_id: int, poll_data,
                          current_user: dict = Depends(LoginRegister.get_current_user)):
        await self.is_admin(current_user)
        await self.user_has_poll_access(current_user, poll_id)
        res = await self.rep.update_poll(poll_id, poll_data)
        return PollCrud.generate_response(success=True, data={'success_delete': res})



    @delete('/delete_poll/{poll_id}')
    async def delete_poll(self, poll_id: int,
                          current_user: dict = Depends(LoginRegister.get_current_user)):
        await self.is_admin(current_user)
        await self.user_has_poll_access(current_user.get('user'), poll_id)
        res = await self.rep.delete_poll(poll_id)
        return PollCrud.generate_response(success=True, data={'success_delete': res})


    @post('/add_question/{poll_id}')
    async def add_question(self, poll_id: int, question,
                           current_user: dict = Depends(LoginRegister.get_current_user)):
        await self.is_admin(current_user)
        await self.user_has_poll_access(current_user, poll_id)
        res = await self.rep.add_question(poll_id, question)
        return PollCrud.generate_response(success=True, data={'success add question': res})



    @delete('/remove_question/{poll_id}/{question_id}')
    async def remove_question(self, poll_id: int, question_id: int,
                              current_user: dict = Depends(LoginRegister.get_current_user)):

        await self.is_admin(current_user)
        await self.user_has_poll_access(current_user, poll_id)
        res = await self.rep.delete_question_in_poll(poll_id, question_id)
        return PollCrud.generate_response(success=True, data={'success remove question': res})


