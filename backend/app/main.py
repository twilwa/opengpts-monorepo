from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import gpt_router, user_router, thread_router
from .db.database import engine
from .db import models
from fastapi.middleware.cors import CORSMiddleware
from .api.api_v1 import auth
import os

app = FastAPI()


app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # TODO: Remove this in production
# models.Base.metadata.drop_all(bind=engine)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(gpt_router.router)
app.include_router(user_router.router)
app.include_router(thread_router.router)
