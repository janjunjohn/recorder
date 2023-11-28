from fastapi import FastAPI
from dotenv import load_dotenv
import os

from routers.routers import router

load_dotenv(".env")

app = FastAPI()

app.include_router(router)
