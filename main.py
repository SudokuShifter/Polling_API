from fastapi import FastAPI, Response, Request

from routers.polls_crud import PollRouter
from routers.reg_auth import LoginRegisterRouter
from routers.answer import AnswerRouter

from repository.polls import PollRepository
from repository.users import UserRepository
from repository.answers import ResultRepository
from fastapi.middleware.cors import CORSMiddleware

from models.db_models import User, UserResult, Poll, Answer
from repository.session_db.session import get_db


app = FastAPI()


poll_rep = PollRepository()
user_rep = UserRepository()
result_rep = ResultRepository()

poll_router = PollRouter(poll_rep)
user_router = LoginRegisterRouter(user_rep)
answer_router = AnswerRouter(result_rep)

app.include_router(poll_router.router, prefix="/polls", tags=["polls"])
app.include_router(user_router.router, prefix="/user", tags=["users"])
app.include_router(answer_router.router, prefix="/answer", tags=["answers"])





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
