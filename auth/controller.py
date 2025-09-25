from fastapi import APIRouter,status
from . import model
from . import service
from  database.core import DbSession

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/signup",status_code=status.HTTP_201_CREATED  )
def signUp(user_signup:model.CreateUser,db:DbSession):
    return service.signUp(db,user_signup)

@router.post("/signin", status_code=status.HTTP_200_OK)
def signIn(user_signin:model.LoginUser,db:DbSession):
    return service.signIn(db,user_signin)
