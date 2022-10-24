from unicodedata import name
from fastapi import FastAPI, status, Depends, HTTPException, Request, Response
from typing import Union, List
from pydantic import BaseModel
import crud
import models
import schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


auth_book_app = FastAPI()


@auth_book_app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


@auth_book_app.post("/authors/", response_model=schemas.Author)
def create_author(user: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.create_author(db=db, author=user)
    return db_author


@auth_book_app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@auth_book_app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    return db_author


@auth_book_app.patch("/authors/{author_id}", response_model=schemas.Author)
def update_author(author: schemas.AuthorUpdate, author_id: int, db: Session = Depends(get_db)):
    db_author = crud.update_author(db, author=author, author_id=author_id)
    return db_author


@auth_book_app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.delete_author(db,  author_id=author_id)
    return db_author


########################################################################################
# Books apis


@auth_book_app.post("/books/{author_id}", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_author_s_book(db=db, book=book, author_id=author_id)


@auth_book_app.get("/books/", response_model=List[schemas.Book])
def read_all_books(authorid: Union[int, None] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if authorid:
        books = crud.get_books(db, skip=skip, limit=limit, author_id=authorid)
    else:
        books = crud.get_books(db, skip=skip, limit=limit, author_id=None)
    return books


@auth_book_app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_book(db, book_id=book_id)
    return db_user


@auth_book_app.patch("/books/{book_id}", response_model=schemas.Book)
def update_Book(book: schemas.BookUpdate, book_id: int, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book=book, book_id=book_id)
    return db_book


@auth_book_app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db,  book_id=book_id)
    return db_book
