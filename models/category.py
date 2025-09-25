from database.core import Base
from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Category (Base):

    __tablename__ = "category"

    id = Column(Integer,autoincrement=True , primary_key= True )
    name = Column(String , unique=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    products = relationship("Product",back_populates="category")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return f"<Category name={self.name}>"