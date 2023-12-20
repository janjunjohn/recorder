from fastapi import FastAPI
from dotenv import load_dotenv
import os

from routers.routers import router
from routers.custom_route import CustomRoute

load_dotenv(".env")

app = FastAPI()
app.router.route_class = CustomRoute

app.include_router(router)
