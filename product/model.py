from pydantic import BaseModel,Field
from typing import Optional,List



class AddProductImage(BaseModel):
    image_url:str =Field(...,max_length=500)
    image_name :Optional[str]

class UpdateProducImage(BaseModel):
    image_url:Optional[str] = Field(default=None,max_length=500)
    image_name:Optional[str] = None

class CreateProduct(BaseModel):
    name:str
    description:str
    category_id:int
    price:int
    sku:Optional[str]
    stock_quantity : int
    images : List[AddProductImage]=[]

class UpdateProduct(BaseModel):
    name:Optional[str] = None
    description:Optional[str] = None 
    category_id:Optional[int] = None
    price:Optional[int] = None
    sku:Optional[str] = None
    stock_quantity :Optional[int] = None
    images:Optional[List[UpdateProducImage]]=None