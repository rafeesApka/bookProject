from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from uuid import uuid4, UUID
from typing import List

from ..db import db
from ..models import BookCreate, BookOut
from ..dependency  import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookOut)
async def create_book(book: BookCreate, user: dict = Depends(get_current_user)):
    book_data = {
        "id": str(uuid4()),
        "title": book.title,
        "author": book.author,
        "genre": book.genre or "",
        "user_id": user["id"],
        "created_at": datetime.utcnow()
    }
    await db.books.insert_one(book_data)
    return book_data

@router.get("/", response_model=List[BookOut])
async def list_books(genre: str = Query(default=None), user: dict = Depends(get_current_user)):
    query = {"user_id": user["id"]}
    if genre:
        query["genre"] = genre
    books = await db.books.find(query).to_list(length=100)
    return books

@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: UUID, user: dict = Depends(get_current_user)):
    book = await db.books.find_one({"id": str(book_id)})
    if not book or book["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", response_model=dict)
async def delete_book(book_id: UUID, user: dict = Depends(get_current_user)):
    book = await db.books.find_one({"id": str(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    await db.books.delete_one({"id": str(book_id)})
    return {"message": "Book deleted successfully"}
