from pydantic import BaseModel,Field
from typing import Optional,List



class AddProductImage(BaseModel):
    image_url:str =Field(...,max_length=500)
    image_name :Optional[str]


class CreateProduct(BaseModel):
    name:str
    description:str
    category_id:int
    price:int
    sku:Optional[str]
    stock_quantity : int
    image : List[AddProductImage]=[]

