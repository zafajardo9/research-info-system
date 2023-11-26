from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.author_repo import AuthorRepository
from app.schema import AuthorSchema
from app.model import Users, Author

class AllInformationService:

    @staticmethod
    async def get_student_count_all(db: Session):
        query = f"SELECT COUNT(*) FROM student;"
        result = await db.execute(query)
        count = result.scalar()
        return count

    @staticmethod
    async def get_student_count_by_course(db: Session, course: str):
        query = f"SELECT COUNT(*) FROM student WHERE course = '{course}';"
        result = db.execute(query)
        count = result.scalar()
        return count
    

    @staticmethod
    async def get_number_of_research_proposal(db):
        query = f"SELECT COUNT(*) FROM research_paper"
        result = db.execute(query)
        count = result.scalar()
        return count