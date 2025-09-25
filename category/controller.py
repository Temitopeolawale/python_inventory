from fastapi import APIRouter, status
from database.core import DbSession
from . import service
from . import model 

router = APIRouter(
    prefix="/category",
    tags=["category"]
)

@router.post("/create",status_code=status.HTTP_201_CREATED)
def CreateCat(create_cat:model.createCategory,db:DbSession,):
    return service.createCategory(db,create_cat)

@router.get("/",status_code=status.HTTP_200_OK)
def GetAll(db:DbSession):
    return service.getAllCategory(db)

@router.get("/{id}",status_code=status.HTTP_200_OK)
def GetById(id:int , db:DbSession):
    return service.getCategoryById(db,id)

@router.put("/update/{id}",status_code=status.HTTP_200_OK,response_model=dict)
def UpdateCat(id:int,update_cat:model.updateCategory,db:DbSession):
    return service.updateCategory(db,id,update_cat)

@router.delete("/{id}",status_code=status.HTTP_200_OK)
def DeleteCat(id:int , db:DbSession):
    return service.deleteCategory(db,id)