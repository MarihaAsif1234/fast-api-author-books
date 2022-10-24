from unicodedata import name
from requests import delete
from sqlalchemy import null
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas
import regex

###################################################################################
# CRUD for authors


def get_author(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(
        models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    db_author = db.query(models.Author).offset(skip).limit(limit).all()
    if len(db_author) == 0:
        raise HTTPException(status_code=404, detail="No Author found")
    return db_author


def create_author(db: Session, author: schemas.AuthorCreate):
    # Check if name entered has any character from A to Z OR is not a blank string
    if(author.name == "" or regex.search('[a-zA-Z]', author.name) is None):
        raise HTTPException(
            status_code=422, detail="Author's name cant be blank and should contain atleast one alphabet from A to Z")
    else:
        db_author = models.Author(name=author.name)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
    return db_author


def update_author(db: Session, author: schemas.AuthorUpdate, author_id: int):
    if(author.name):
        if(regex.search('[a-zA-Z]', author.name) is None):
            raise HTTPException(
                status_code=422, detail="Author's name cant be blank and should contain atleast one alphabet from A to Z")
        else:
            db_author = db.query(models.Author).filter(
                models.Author.id == author_id).first()
            author_data = author.dict(exclude_unset=True)
            if db_author:
                for key, value in author_data.items():
                    setattr(db_author, key, value)
                db.add(db_author)
                db.commit()
                db.refresh(db_author)
    else:
        raise HTTPException(
            status_code=422, detail="Empty Json")
    return db_author


def delete_author(db: Session,  author_id: int):
    db_author = db.query(models.Author).filter(
        models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    else:
        db.delete(db_author)
        db.commit()
    return {"deleted": True}

#####################################################################################

# CRUD for books


def get_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(
        models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: int = None):
    if author_id is None:
        books = db.query(models.Book).offset(skip).limit(limit).all()
    else:
        books = db.query(models.Book).filter(
            models.Book.author_id == author_id).all()
    if len(books) == 0:
        raise HTTPException(status_code=404, detail="Books not found")
    return books


def create_author_s_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db_author = get_author(db, author_id=author_id)
    if(book.name == "" or regex.search('[a-zA-Z]', book.name) is None):
        raise HTTPException(
            status_code=422, detail="Book's name cant be blank and should contain atleast one alphabet from A to Z")
    else:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    return db_book


def update_book(db: Session, book: schemas.BookUpdate, book_id: int):
    db_book = db.query(models.Book).filter(
        models.Book.id == book_id).first()
    if book.name:
        if db_book:
            if(book.name == "" or regex.search('[a-zA-Z]', book.name) is None):
                raise HTTPException(
                    status_code=422, detail="Book's name cant be blank and should contain atleast one alphabet from A to Z")
            else:
                book_data = book.dict(exclude_unset=True)
                for key, value in book_data.items():
                    setattr(db_book, key, value)
                db.add(db_book)
                db.commit()
                db.refresh(db_book)
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    else:
        raise HTTPException(status_code=422, detail="Empty Json")
    return db_book


def delete_book(db: Session,  book_id: int):
    db_book = db.query(models.Book).filter(
        models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        db.delete(db_book)
        db.commit()
    return {"deleted": True}


#####################################################################################
