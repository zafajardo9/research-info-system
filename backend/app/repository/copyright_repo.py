
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
from app.model.copyright import CopyRight

from app.config import commit_rollback, db


class CopyrightRepository(BaseRepo):
    model = CopyRight


    #getting manuscript by research ID
    @staticmethod
    async def get_by_research_paper_id(db: Session, research_paper_id: str) -> CopyRight:
        query = select(CopyRight).filter(CopyRight.research_paper_id == research_paper_id)
        result = await db.execute(query)
        return result.scalars().first()
    


    #getting ethics by id
    @staticmethod
    async def get_copyright_by_id(db: Session, copyright_id: str) -> CopyRight:
        query = select(CopyRight).filter(CopyRight.id == copyright_id)
        result = await db.execute(query)
        return result.scalars().first()
    
    
    @staticmethod
    async def update_copyright(db: AsyncSession, copyright_id: str, **kwargs):
        copyright = await CopyrightRepository.get_copyright_by_id(db, copyright_id)

        if copyright:
            await CopyrightRepository.update(db, copyright, **kwargs)
        else:
            raise HTTPException(status_code=404, detail="Manuscript data not found")

    @staticmethod
    async def delete_copyright_id(db: Session, copyright_id: str) -> bool:
        query = delete(CopyRight).where(CopyRight.id == copyright_id)
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0