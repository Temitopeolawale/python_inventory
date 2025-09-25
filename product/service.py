from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.product.product import Product
from models.product.product_image import ProductImage
from . import model
from sqlalchemy.exc import IntegrityError
import logging
from typing import List


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

        for images in create_product.image:
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
        logger.info(f"server:{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error"
        )
