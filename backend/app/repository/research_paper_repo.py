
from typing import List
from app.schema import AuthorSchema, ResearchPaperSchema

from sqlalchemy import insert, update, delete, or_, text, func, column
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.research_paper import ResearchPaper, Author

from app.config import db, commit_rollback




class ResearchPaperRepository:
    
    @staticmethod
    async def create(research_paper: ResearchPaperSchema):
        research_paper = ResearchPaper(**research_paper.dict())
        db.add(research_paper)
        await db.commit()
        await db.refresh(research_paper)
        return research_paper

    @staticmethod
    async def get_by_id(id: int):
        query = select(ResearchPaper).where(ResearchPaper.id == id)
        result = await db.execute(query)
        research_paper = result.scalar_one_or_none()
        return research_paper

    @staticmethod
    async def get_all():
        query = select(ResearchPaper)
        result = await db.execute(query)
        research_papers = result.scalars().all()
        return research_papers

    @staticmethod
    async def update(id: int, updated_paper: ResearchPaper):
        db.update(ResearchPaper).where(ResearchPaper.id == id).values(title=updated_paper.title, content=updated_paper.content)
        await db.commit()

    @staticmethod
    async def delete(id: int):
        db.delete(ResearchPaper).where(ResearchPaper.id == id)
        await db.commit()