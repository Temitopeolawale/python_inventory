from fastapi import HTTPException,status
from models.user import User
from sqlalchemy.orm import Session, defer




def getUserById(id:int,db:Session):
    try:
        user = db.query(User).options(defer(User.password_hash)).filter(User.id == id).first()

        if not user:
          raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        return user 
    except HTTPException  :
       raise
    except Exception as e :
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail='Failed to fetch user {e}'
       )