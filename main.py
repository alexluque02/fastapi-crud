from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import Base

app = FastAPI()


class Book(Base):
    __tablename__ = "books"
    id: int
    title: str
    author: str
    year: int


class UpdateBookDto(BaseModel):
    title: Optional[str]
    author: Optional[str]
    year: Optional[int]


bookList: List[Book] = [
    Book(
        id=1,
        title="Mares revueltos",
        author="Doe",
        year=2002,
    ),
    Book(
        id=2,
        title="Tinieblas",
        author="Pepe",
        year=2002,
    ),
    Book(
        id=3,
        title="Peee",
        author="Jota",
        year=2002,
    ),
    Book(
        id=4,
        title="Johdsfan",
        author="Juan",
        year=2002,
    ),
]


@app.get("/books/")
async def get_books():
    return bookList


@app.get("/books/{id_book}")
async def get_book(id_book: int):
    for book in bookList:
        if book.id == id_book:
            return book
    raise HTTPException(
        status_code=404, detail=f"Get book failed, id {id_book} not found."
    )


@app.post("/books/create")
async def create_book(book: Book):
    bookList.append(book)
    return {"id": book.id}


@app.delete("/books/delete/{id_book}")
async def delete_book(id_book: int):
    for book in bookList:
        if book.id == id_book:
            bookList.remove(book)
            return book
    raise HTTPException(
        status_code=404, detail=f"Delete book failed, id {id_book} not found."
    )


@app.put("/books/update/{id_book}")
async def update_book(book_update: UpdateBookDto, id_book: int):
    for book in bookList:
        if book.id == id_book:
            if book_update.title is not None:
                book.title = book_update.title
            if book_update.author is not None:
                book.author = book_update.author
            if book_update.year is not None:
                book.year = book_update.year
            return book
    raise HTTPException(status_code=404, detail=f"Could not find book with id: {id}")
