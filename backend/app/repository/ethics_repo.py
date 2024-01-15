
from typing import List, Optional
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import commit_rollback, db

from app.repository.base_repo import BaseRepo
from app.model.ethics import Ethics
from app.model.research_paper import ResearchPaper, Status
from app.model import CopyRight, FullManuscript



class EthicsRepository(BaseRepo):
    model = Ethics

    #getting research paper
    @staticmethod
    async def get_by_research_paper_id(db: Session, research_paper_id: str) -> Ethics:
        query = select(Ethics).filter(Ethics.research_paper_id == research_paper_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    #getting ethics by id
    @staticmethod
    async def get_ethics_by_id(db: Session, ethics_id: str) -> Ethics:
        query = select(Ethics).filter(Ethics.id == ethics_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    
    @staticmethod
    async def update_ethics(db: AsyncSession, ethics_id: str, **kwargs):
        ethics = await EthicsRepository.get_ethics_by_id(db, ethics_id)

        if ethics:
            await EthicsRepository.update(db, ethics, **kwargs)
        else:
            raise HTTPException(status_code=404, detail="Ethics data not found")

        

    @staticmethod
    async def delete_by_ethics_id(db: Session, ethics_id: str) -> bool:
        query = delete(Ethics).where(Ethics.id == ethics_id)
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0
    
    
    @staticmethod
    async def update_status_ethics(db: Session, research_paper_id: str, new_status: Status) -> Ethics:
        # Fetch the research paper
        result = await db.execute(select(Ethics).where(Ethics.id == research_paper_id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            research_paper.status = new_status
            await db.commit()
            db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Ethics not found")
        
    @staticmethod
    async def update_status_manu(db: Session, id: str, new_status: Status) -> Ethics:
        # Fetch the research paper
        result = await db.execute(select(FullManuscript).where(FullManuscript.id == id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            research_paper.status = new_status
            await db.commit()
            db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Manuscript not found")
        
    @staticmethod
    async def update_status_copy(db: Session, id: str, new_status: Status) -> Ethics:
        # Fetch the research paper
        result = await db.execute(select(CopyRight).where(CopyRight.id == id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            research_paper.status = new_status
            await db.commit()
            db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Copyright not found")