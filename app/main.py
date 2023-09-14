
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from routers import post, users, auth, vote
from .config import settings
# models.Base.metadata.create_all(bind=engine) alembic doing this function
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# data model


@app.get("/")
async def root():
    return {"message": "Welcome to my program"}
