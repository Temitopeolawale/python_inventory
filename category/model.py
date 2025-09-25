from pydantic import BaseModel
from typing import Optional

class createCategory(BaseModel):
    name:str
    description:str


class updateCategory(BaseModel):
    name:Optional[str] = None
    description:Optional[str]=None


