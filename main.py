from fastapi import FastAPI

from routers.polls_crud import PollCrud
from routers.reg_auth import LoginRegister
from routers.answer import AnswerResult

from repository.polls import PollRepository
from repository.users import UserRepository
from repository.answers import ResultRepository

from models.db_models import User, UserResult, Poll, Answer

app = FastAPI()

poll_rep = PollRepository()
user_rep = UserRepository()
result_rep = ResultRepository()

poll_router = PollCrud(model=Poll, rep=poll_rep)
user_router = LoginRegister(model=User, rep=user_rep)
answer_router = AnswerResult(model=Answer, rep=result_rep)

app.include_router(poll_router, prefix="/polls", tags=["polls"])
app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(answer_router, prefix="/answer", tags=["answers"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)