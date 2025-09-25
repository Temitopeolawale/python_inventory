from database.core import Base
from sqlalchemy import Column,String,Boolean,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class ProductImage(Base):
    __tablename__ ="product_image"
    id = Column(Integer, autoincrement=True , primary_key=True,index=True)
    product_id = Column(Integer,ForeignKey("product.id"))
    image_url = Column(String,nullable= False)
    image_name = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    product = relationship("Product",back_populates="image")

    def to_dict (self):
        return {c.name:getattr(self,c.name) for c in self.__table__.columns}
    
    def __repr__(self):
        return f"<ProductImage  name={self.image_name}>"