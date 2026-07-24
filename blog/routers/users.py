from typing import List
from fastapi import APIRouter, Depends
from blog import models, schemas
from blog.database import SessionLocal, engine
from sqlalchemy.orm import Session
from blog.hashing import Hash

router = APIRouter()

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally : 
        db.close()

@router.post('/create_user',tags=['users'])
def create_user(request : schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.hash_pass(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}', response_model=schemas.ShowUser,tags=['users'])
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user