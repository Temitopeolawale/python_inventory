from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.category import Category
from sqlalchemy.exc import IntegrityError
from . import model
import logging 

logging.basicConfig(level=logging.info)
logger =logging.getLogger(__name__)


def createCategory(db:Session, create_category:model.createCategory):
    try:
        newCategory = Category(
            name = create_category.name,
            description = create_category.description
        )

        logger.info("category created")

        db.add(newCategory)
        db.commit()
        db.refresh(newCategory)

        return {
            "message":"Category Created Successfully",
            "category":newCategory.to_dict()
        }
    except IntegrityError as e:
        db.rollback()
        logger.error(f"integrity error :{e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exist"
        )
    except HTTPException:
        db.rollback()
        raise 
    except Exception as e :
        db.rollback()
        logger.info(f"server:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

def getAllCategory(db:Session):
        category=db.query(Category).all()
        return {
            "message":"success",
            "categories":[cat.to_dict() for cat in category]
        }

def getCategoryById(db:Session,id:int):
    try:
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="category does not exist"
            )
        return {
            "message":"successful",
            "category":category.to_dict()
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.info(f"server:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error "
        )

def updateCategory(db: Session,id: int,update_category: model.updateCategory):
    try:
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="category does not exist"
            )
        if update_category.name:
            cat_exist = db.query(Category).filter(Category.name == update_category.name).first()
            if cat_exist and cat_exist.id !=id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="category already exists"
                )
        db.query(Category).filter(Category.id == id ).update(update_category.dict(exclude_unset=True))
        db.commit()
        newcategory = db.query(Category).filter(Category.id == id).first()

        return {
            "message": "Field Updated Successfully",
            "category": {
                "id": newcategory.id,
                "name": newcategory.name,
                "description": newcategory.description
            }
        }
    except HTTPException:
        db.rollback()
        raise 
    except Exception as e :
        db.rollback()
        logger.error(f"server:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error "
        )

def deleteCategory(db:Session , id:int ):
    try:
        category = db.query(Category).filter(Category.id == id).delete()
        if not category:
           raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="category does not exist"
            )
        else:
            db.commit()
            return "successful"
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.info(f"server:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        )