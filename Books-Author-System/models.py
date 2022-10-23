from unicodedata import name
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# One to Many relationship between author and books


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  index=True, nullable=False)

    books = relationship(
        "Book", back_populates="bookauthor", cascade="all, delete")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("author.id"))

    bookauthor = relationship("Author", back_populates="books")
