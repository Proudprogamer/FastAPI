from typing import List
from fastapi import FastAPI, Depends
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import blog, users

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally : 
        db.close()

@app.get('/')
def home():
    return "Home"


app.include_router(blog.router)
app.include_router(users.router)



