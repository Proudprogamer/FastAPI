from typing import List
from fastapi import APIRouter, Depends
from blog import models, schemas
from blog.database import SessionLocal, engine
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally : 
        db.close()

@router.post('/new-blog', status_code=201, tags=['blogs'])
def post_blog(request : schemas.BlogType, db : Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/blogs', response_model=List[schemas.ShowBlog],tags=['blogs'])
def get_blogs(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get('/blog/{id}', response_model=schemas.ShowBlog,tags=['blogs'])
def get_blog(id: int, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog

@router.delete('/blog/{id}',tags=['blogs'])
def del_blog(id: int, db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'deleted'}

@router.put('/blog/{id}',tags=['blogs'])
def update_blog(id: int,request : schemas.BlogType, db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update({
        models.Blog.title: request.title,
        models.Blog.body: request.body
    }, synchronize_session=False)
    db.commit()
    return {'updated'}