from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from routers.reg_auth import LoginRegisterRouter
from repository.polls import PollRepository


class AnswerRouter:

    def __init__(self, rep):
        self.router = APIRouter()
        self.rep = rep
        self.router.add_api_route('/my_results', self.get_my_results, methods=['GET'])
        self.router.add_api_route('/get_answer/{question_id}', self.post_answer, methods=['POST'])
        self.router.add_api_route('/get_answer_for_unauthorize/{question_id}', self.post_answer_for_unauthorize, methods=['POST'])
        self.router.add_api_route('/create_result_for_poll/{poll_id}', self.post_result_for_poll, methods=['POST'])


    @staticmethod
    def generate_response(success: bool, data=None, detail=None):
        return JSONResponse(content={"success": success, "data": data, "detail": detail})


    @staticmethod
    async def is_user(current_user: dict) -> bool:
        if current_user['role'] == 'user':
            return True
        raise HTTPException(status_code=403, detail='Not permission')


    async def get_my_results(self, current_user: dict = Depends(LoginRegisterRouter.get_current_user)):
        await self.is_user(current_user)
        user_id = current_user['id']
        results = await self.rep.get_all_results_by_user_id(user_id=user_id)
        polls = [{'polls': PollRepository.get_poll_by_id(i.poll_id),
                  'questions': PollRepository.get_questions_by_poll_id(i.poll_id)}
                   for i in results]
        return AnswerRouter.generate_response(success=True, data=polls, detail=None)


    async def post_answer(self, question_id: str, answer,
                          current_user: dict = Depends(LoginRegisterRouter.get_current_user)):

        await self.is_user(current_user)
        question = await self.rep.get_question(question_id)
        if self.rep.answer_for_question(answer.answer, question_id):
            res = await self.rep.add_result_for_question(True, answer.answer, question, user=current_user['id'])
            return AnswerRouter.generate_response(success=True, data=res, detail=None)

        res = await self.rep.add_result_for_question(False, answer.answer, question, user=current_user['id'])
        return AnswerRouter.generate_response(success=False, data=res, detail=None)


    async def post_answer_for_unauthorize(self, question_id: str, answer):
        question = await self.rep.get_question(question_id)

        if self.rep.answer_for_question(answer.answer, question_id):
            res = await self.rep.add_result_for_question(True, answer.answer, question)
            return AnswerRouter.generate_response(success=True, data=res, detail=None)

        res = await self.rep.add_result_for_question(False, answer.answer, question)
        return AnswerRouter.generate_response(success=False, data=res, detail=None)


    async def post_result_for_poll(self, poll_id: str,
                                   current_user: dict = Depends(LoginRegisterRouter.get_current_user)):

        await self.is_user(current_user)
        if PollRepository.poll_is_active(poll_id):
            questions = await self.rep.get_question(poll_id)
            res = self.rep.generate_result(questions, current_user['id'])
            return AnswerRouter.generate_response(success=True, data=res, detail=None)
        raise HTTPException(status_code=403, detail='Poll is not active')
