from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from starlette.status import HTTP_201_CREATED

from db import Base, engine, Session, get_session

app = FastAPI()


class BookSQL(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)


class Book(BaseModel):
    id: Optional[int]
    title: str
    author: str
    year: int

    class Config:
        orm_mode = True


#bookList: List[BookSQL] = [
#    BookSQL(
#        id=1,
#        title="Mares revueltos",
#        author="Doe",
#        year=2002,
#    ),
#    BookSQL(
#        id=2,
#        title="Tinieblas",
#        author="Pepe",
#        year=2002,
#    ),
#    BookSQL(
#        id=3,
#        title="Peee",
#        author="Jota",
#        year=2002,
#    ),
#    BookSQL(
#        id=4,
#        title="Johdsfan",
#        author="Juan",
#        year=2002,
#    ),
#]


#@app.get("/books/")
#async def get_books():
#    return bookList

@app.on_event('startup')
def create_db():
    Base.metadata.create_all(bind=engine)


#@app.get("/books/{id_book}")
#async def get_book(id_book: int):
#    for book in bookList:
#        if book.id == id_book:
#            return book
#    raise HTTPException(
#        status_code=404, detail=f"Get book failed, id {id_book} not found."
#    )


@app.post("/books/create", response_model=BookSQL, status_code=HTTP_201_CREATED)
async def create_book(book: Book, session: Session = Depends(get_session)) -> BookSQL:
    #bookList.append(book)
    book_sql = BookSQL(title=book.title, autor=book.author, year=book.year)
    session.add(book_sql)
    session.commit()
    return BookSQL.from_orm(book_sql)


#@app.delete("/books/delete/{id_book}")
#async def delete_book(id_book: int):
#    for book in bookList:
#        if book.id == id_book:
#            bookList.remove(book)
#            return book
#    raise HTTPException(
#        status_code=404, detail=f"Delete book failed, id {id_book} not found."
#    )


#@app.put("/books/update/{id_book}")
#async def update_book(book_update: Book, id_book: int):
#    for book in bookList:
#        if book.id == id_book:
#            if book_update.title is not None:
#                book.title = book_update.title
#            if book_update.author is not None:
#                book.author = book_update.author
#            if book_update.year is not None:
#                book.year = book_update.year
#            return book
#    raise HTTPException(status_code=404, detail=f"Could not find book with id: {id}")
