from fastapi import HTTPException,status
from models.user import User
from . import jwt_handler
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from passlib.context import CryptContext
from . import model
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def hashed_password (password:str):
    return bcrypt_context.hash(password)

def verify_password(password:str , hashed_password):
    return bcrypt_context.verify(password,hashed_password)

def signUp (db:Session, create_user:model.CreateUser):
    try:
        hash = hashed_password(create_user.password)
        logger.info("password was hashed ")

        newUser = User(
            email = create_user.email,
            first_name = create_user.first_name,
            last_name = create_user.last_name,
            password_hash = hash
        )
        logger.info("user created")

        db.add(newUser)
        db.commit()
        db.refresh(newUser)

        logger.info("user saved to the da")

        token = jwt_handler.generate_tokens(
            user_id=str(newUser.id),
            username=newUser.email,
            first_name=newUser.first_name,
            last_name=newUser.last_name
        )
        logger.info("did this run")
        return{
            "User":newUser,
            "Token":token
        }
    except IntegrityError as e :
        db.rollback()
        logger.error(f"Integrity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exist"
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating user"
        )
    

def signIn(db:Session,user_signIn:model.LoginUser):
    user = db.query(User).filter(User.email == user_signIn.email).first()
    try:
        if not user or not verify_password(user_signIn.password,user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password  "
            )
        token = jwt_handler.generate_tokens(
            user_id=str(user.id),
            username=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )

        return {
            "message":"User login successful ",
            "token":token 
        }

    except HTTPException:
        raise
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        )





