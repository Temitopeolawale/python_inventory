from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,DateTime
from database.core import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Product(Base):
    __tablename__="product"

    id = Column(Integer,autoincrement=True, primary_key=True , index=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"))
    price = Column(Integer, nullable=False)
    sku = Column(String,unique=True)
    stock_quantity = Column(Integer , default=0)
    is_active = Column(Boolean ,default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now() ,onupdate=func.now())

    image = relationship("ProductImage",back_populates="product",cascade="all, delete-orphan")
    category = relationship("Category",back_populates='products')
    

    def to_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        result['images'] = [img.to_dict() for img in self.image]
        return result
    
    def __repr__(self):
        return f"<Product name={self.name}>"