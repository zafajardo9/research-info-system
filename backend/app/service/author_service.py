from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.author_repo import AuthorRepository
from app.schema import AuthorSchema
from app.model import Users, Author

class AuthorService:

    @staticmethod
    async def create_author(
        db: Session, 
        author_data: AuthorSchema, 
        username: str
    ):
        _author_id = str(uuid4())
        
        # Mapping request data to class entity table
        _author = await AuthorRepository.create(
            db, 
            id=_author_id,
            name=author_data.name,
            user_id=author_data.user_id
        )
        
        return _author

    @staticmethod
    async def get_author(
        db: Session, 
        author_id: str
    ):
        _author = await AuthorRepository.get(db, author_id)
        if not _author:
            raise HTTPException(status_code=404, detail="Author not found")
        return _author
