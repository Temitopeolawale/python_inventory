from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.product.product import Product
from models.product.product_image import ProductImage
from . import model
from sqlalchemy.exc import IntegrityError
import logging


logging.basicConfig(level=logging.info)
logger=logging.getLogger(__name__)

def createproduct(db:Session,create_product:model.CreateProduct ):
    try:
        product = db.query(Product).filter(Product.name == create_product.name).first()
        if product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exist"
            )
        newproduct = Product(
            name = create_product.name,
            description = create_product.description,
            category_id = create_product.category_id,
            price = create_product.price,
            sku = create_product.sku,
            stock_quantity = create_product.stock_quantity
        )
        db.add(newproduct)
        db.flush()

        for images in create_product.images:
            product_images = ProductImage(
                product_id = newproduct.id,
                image_url = images.image_url,
                image_name= images.image_name
            )
            db.add(product_images)
        db.commit()
        db.refresh(newproduct)
        return newproduct
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
        logger.error(f"server:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )

def getAllProduct(db:Session):
    try:
        product = db.query(Product).all()
        return{
            "message":"Successful",
            "products":[prod.to_dict() for prod in product]
        }
    except Exception as e :
        logger.error(f"server:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error "
        )

def getProductById(db:Session,id:int):
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return{
            "message":"successful",
            "product":product.to_dict()
        }
    except Exception as e :
        logger.error(f"server:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="server error"
        )
    
def updateProduct(db:Session,id:int,update_product:model.UpdateProduct):
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="product not found"
            )
        if update_product.name:
            prod_exist = db.query(Product).filter(Product.name == update_product.name).first()
            if prod_exist and prod_exist.id !=id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Product already exist"
                )
            db.query(Product).filter(Product.id == id).update(update_product.dict(exclude_unset=True))
        if update_product.images:
            image_update = db.query(ProductImage).filter(ProductImage.product_id == id).all()
            if not image_update:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="product id not found"
                )
            db.query(ProductImage).filter(ProductImage.product_id == id).update(update_product.images)
        db.commit()
        updated_product = db.query(Product).filter(Product.id == id).first()
        return{
            "message":"Product updated sussessfully",
            "product":updated_product.to_dict()
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