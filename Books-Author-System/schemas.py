from typing import List, Union, Optional
from unicodedata import name

from pydantic import BaseModel


class BookBase(BaseModel):
    name: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class BookUpdate(BaseModel):
    name: Optional[str] = None


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
