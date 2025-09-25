from fastapi import FastAPI
from api import register_routes
from models import user
from database.core import engine,Base
app = FastAPI()

Base.metadata.create_all(bind=engine)

register_routes(app)