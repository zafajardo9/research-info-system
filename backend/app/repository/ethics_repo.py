
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



class EthicsRepository(BaseRepo):
    model = Ethics



    @staticmethod
    async def get_by_research_paper_id(db: Session, research_paper_id: str) -> Ethics:
        query = select(Ethics).filter(Ethics.research_paper_id == research_paper_id)
        result = await db.execute(query)
        return result.scalars().first()
    

    


    @staticmethod
    async def update(db: Session, ethics: Ethics) -> Ethics:
        db.add(ethics)
        await db.commit()
        await db.refresh(ethics)
        return ethics

    # @staticmethod
    # async def delete_by_research_paper_id(db: Session, research_paper_id: str) -> bool:
    #     ethics_data = await db.query(Ethics).filter(Ethics.research_paper_id == research_paper_id).first()

    #     if ethics_data:
    #         db.delete(ethics_data)
    #         await db.commit()
    #         return True
    #     else:
    #         return False
        

    @staticmethod
    async def delete_by_ethics_id(db: Session, ethics_id: str) -> bool:
        query = delete(Ethics).where(Ethics.id == ethics_id)
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0