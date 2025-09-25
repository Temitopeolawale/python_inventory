from database.core import Base
from sqlalchemy import Column,String,Integer




class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer,primary_key=True, autoincrement=True , index=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable= False)
    last_name = Column(String, nullable= False)
    password_hash = Column(String, nullable=False)


def __repr__(self):
    return f"<User email={self.email},first_name={self.first_name},last_name={self.last_name},password_hash={self.password_hash} >"