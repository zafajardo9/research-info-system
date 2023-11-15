from datetime import datetime
import math
from typing import List
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db
from app.model.research_paper import Author, ResearchPaper
from app.repository.base_repo import BaseRepo
from app.schema import PageResponse, ResearchPaperCreate


class ResearchPaperRepository(BaseRepo):
    model = ResearchPaper


    @staticmethod
    async def get_by_id(db: Session, research_paper_id: str) -> ResearchPaper:
        query = select(ResearchPaper).where(ResearchPaper.id == research_paper_id)
        return (await db.execute(query)).scalar_one_or_none()
    

    @staticmethod
    async def get_all(db: Session) -> List[ResearchPaper]:
        """
        Get all research papers from the database.
        """
        query = select(ResearchPaper)
        return (await db.execute(query)).scalars().all()
    
    @staticmethod
    async def delete(research_id: str):
        """ delete research data by id """

        # Delete related records in the Author table first
        await db.execute(delete(Author).where(Author.research_paper_id == research_id))

        # Now, delete the research paper
        query = delete(ResearchPaper).where(ResearchPaper.id == research_id)
        await db.execute(query)
        await commit_rollback()
