from fastapi import FastAPI
from .routers import tasks
from .database import engine
from .api_models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)