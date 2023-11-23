
from typing import List, Optional
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.base_repo import BaseRepo
from app.model.full_manuscript import FullManuscript

from app.config import commit_rollback, db


class ManuscriptRepository(BaseRepo):
    model = FullManuscript


    #getting manuscript by research ID
    @staticmethod
    async def get_by_research_paper_id(db: Session, research_paper_id: str) -> FullManuscript:
        query = select(FullManuscript).filter(FullManuscript.research_paper_id == research_paper_id)
        result = await db.execute(query)
        return result.scalars().first()
    


    #getting ethics by id
    @staticmethod
    async def get_manuscript_by_id(db: Session, manuscript_id: str) -> FullManuscript:
        query = select(FullManuscript).filter(FullManuscript.id == manuscript_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    
    @staticmethod
    async def update_manuscript(db: AsyncSession, manuscript_id: str, **kwargs):
        manuscript = await ManuscriptRepository.get_manuscript_by_id(db, manuscript_id)

        if manuscript:
            await ManuscriptRepository.update(db, manuscript, **kwargs)
        else:
            raise HTTPException(status_code=404, detail="Manuscript data not found")

    @staticmethod
    async def delete_manuscript_id(db: Session, ethics_id: str) -> bool:
        query = delete(FullManuscript).where(FullManuscript.id == ethics_id)
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0