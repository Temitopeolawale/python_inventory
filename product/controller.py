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

@router.get("/",status_code=status.HTTP_200_OK)
def GetAllProduct(db:DbSession):
    return service.getAllProduct(db)

@router.get("/{id}",status_code=status.HTTP_200_OK)
def GetProductById(id:int,db:DbSession):
    return service.getProductById(db,id)

@router.put('/{id}',status_code=status.HTTP_200_OK)
def UpdateProduct(id:int,update_product:model.UpdateProduct,db:DbSession):
    return service.updateProduct(db,id,update_product)