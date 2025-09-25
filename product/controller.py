from fastapi import APIRouter,status
from . import service 
from database.core import DbSession
from . import model 


router = APIRouter(
    prefix="/product",
    tags=["product"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def CreateProduct(create_product:model.CreateProduct, db:DbSession):
    return service.createproduct(db,create_product)