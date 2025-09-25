from fastapi import FastAPI
from auth.controller import router as auth_router
from user.controller import router as user_router
from category.controller import router as cat_router
from product.controller import router as prod_router

def register_routes(app:FastAPI):
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(cat_router)
    app.include_router(prod_router)