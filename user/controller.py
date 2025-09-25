from fastapi import APIRouter,status, Depends
from . import service
from database.core import DbSession
from auth.jwt_handler import get_current_user_id

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get("/me",status_code=status.HTTP_200_OK)
def GetUserId(db:DbSession,id:int =Depends(get_current_user_id)):
    return service.getUserById(id,db)