from typing import List
from fastapi import FastAPI, Depends
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session


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

@app.post('/new-blog', status_code=201)
def post_blog(request : schemas.BlogType, db : Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs', response_model=List[schemas.ShowBlog])
def get_blogs(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', response_model=schemas.ShowBlog)
def get_blog(id: int, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog

@app.delete('/blog/{id}')
def del_blog(id: int, db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'deleted'}

@app.put('/blog/{id}')
def update_blog(id: int,request : schemas.BlogType, db : Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update({
        models.Blog.title: request.title,
        models.Blog.body: request.body
    }, synchronize_session=False)
    db.commit()
    return {'updated'}