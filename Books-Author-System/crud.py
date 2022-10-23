from unicodedata import name
from requests import delete
from sqlalchemy import null
from sqlalchemy.orm import Session

import models
import schemas

# CRUD for authors


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def del_author(db: Session, author_id: int):
    db_book = db.query(models.Author).filter(
        models.Author.id == author_id).delete()
    db.commit()
    db.refresh(db_book)
    return db_book


def update_author(db: Session, author: schemas.AuthorUpdate, author_id: int):
    db_author = db.query(models.Author).filter(
        models.Author.id == author_id).first()
    author_data = author.dict(exclude_unset=True)
    if db_author:
        for key, value in author_data.items():
            setattr(db_author, key, value)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session,  author_id: int):
    db_author = db.query(models.Author).filter(
        models.Author.id == author_id).first()
    print("yahan aata")
    if db_author is None:
        return {"deleted": "Not found"}
    if db_author:
        db.delete(db_author)
        db.commit()
        print("yahan bhi  aata")
    print("bbb yahan aata")
    return {"deleted": True}

#####################################################################################

# CRUD for authors


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: int = None):
    if author_id is None:
        return db.query(models.Book).offset(skip).limit(limit).all()
    else:
        return db.query(models.Book).filter(models.Book.author_id == author_id).all()


def create_author_s_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def del_book(db: Session, author_id: int):
    db_book = db.query(models.Book).filter(
        models.Author.id == author_id).delete()
    db.commit()
    db.refresh(db_book)
    return db_book


#####################################################################################
