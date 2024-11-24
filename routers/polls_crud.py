from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from routers.reg_auth import LoginRegisterRouter
from schemas.poll import PollInFirst, PollInChange, QuestionIn
from repository.session_db.session import get_db


class PollRouter:

    def __init__(self, rep):
        self.router = APIRouter()
        self.rep = rep
        self.router.add_api_route('/get_polls',
                                  self.get_all_polls, methods=['GET'])
        self.router.add_api_route('/get_poll/{poll_id}',
                                  self.get_poll, methods=['GET'])
        self.router.add_api_route('/create_poll',
                                  self.create_poll, methods=['POST'])
        self.router.add_api_route('/update_poll/{poll_id}',
                                  self.update_poll, methods=['PUT'])
        self.router.add_api_route('/delete_poll/{poll_id}',
                                  self.delete_poll, methods=['DELETE'])
        self.router.add_api_route('/add_question/{poll_id}',
                                  self.add_question, methods=['POST'])
        self.router.add_api_route('/remove_question/{poll_id}/{question_id}',
                                  self.remove_question, methods=['DELETE'])


    @staticmethod
    async def is_admin(current_user: dict) -> bool:
        if current_user['role'] == 'admin':
            return True
        raise HTTPException(status_code=403, detail='Not permissions')


    async def user_has_poll_access(self, current_user: dict, poll_id: int,
                                   db: AsyncSession = Depends(get_db)) -> bool:

        if not await self.rep.polls_by_user(current_user, poll_id, db):
            raise HTTPException(status_code=403, detail='Not permissions')
        return True


    @staticmethod
    def generate_response(success: bool, data=None, detail=None) -> JSONResponse:
        return JSONResponse(content={'success': success, 'data': data, 'detail': detail})


    async def get_all_polls(self, db: AsyncSession = Depends(get_db)):

        polls = await self.rep.get_all_polls(db)
        return PollRouter.generate_response(success=True,
                                            data={'polls': polls})


    async def get_poll(self, poll_id: int, db: AsyncSession = Depends(get_db)):

        poll = await self.rep.get_poll_by_id(poll_id, db)
        questions_full = await self.rep.get_questions_by_poll_id(poll_id, db)

        return PollRouter.generate_response(success=True,
                                            data={'poll': f'{poll}', 'questions': f'{questions_full}'})


    async def create_poll(self, poll: PollInFirst,
                          current_user: dict = Depends(LoginRegisterRouter.get_current_user),
                          db: AsyncSession = Depends(get_db)):
        await self.is_admin(current_user)
        res = await self.rep.create_poll(current_user['id'], poll, db)

        return PollRouter.generate_response(success=True,
                                            data={'success_create': res})


    async def update_poll(self, poll_id: int, poll_data: PollInChange,
                          current_user: dict = Depends(LoginRegisterRouter.get_current_user),
                          db: AsyncSession = Depends(get_db)):

        await self.is_admin(current_user)
        await self.user_has_poll_access(current_user['id'], poll_id, db)
        res = await self.rep.update_poll(poll_id, poll_data, db)

        return PollRouter.generate_response(success=True,
                                            data={
                                                'success_update': f'{res}',
                                                'data': [poll_data.title, str(poll_data.date_end)]})


    async def delete_poll(self, poll_id: int,
                          current_user: dict = Depends(LoginRegisterRouter.get_current_user),
                          db: AsyncSession = Depends(get_db)):

        await self.is_admin(current_user)
        await self.user_has_poll_access(current_user['id'], poll_id, db)
        res = await self.rep.delete_poll(poll_id, db)

        return PollRouter.generate_response(success=True,
                                            data={'success_delete': res})


    async def add_question(self, poll_id: int, question: QuestionIn,
                           current_user: dict = Depends(LoginRegisterRouter.get_current_user),
                           db: AsyncSession = Depends(get_db)):

        await self.is_admin(current_user)
        await self.user_has_poll_access(current_user['id'], poll_id, db)
        res = await self.rep.add_question_in_poll(poll_id, question, db)

        return PollRouter.generate_response(success=True,
                                            data={'success add question': res, 'data': question.title})


    async def remove_question(self, poll_id: int, question_id: int,
                              current_user: dict = Depends(LoginRegisterRouter.get_current_user),
                              db: AsyncSession = Depends(get_db)):

        await self.is_admin(current_user)
        await self.user_has_poll_access(current_user['id'], poll_id, db)
        res = await self.rep.delete_question_in_poll(poll_id, question_id, db)

        return PollRouter.generate_response(success=True,
                                            data={'success remove question': res})


