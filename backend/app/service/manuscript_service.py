from datetime import datetime
from sqlalchemy import join
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from app.schema import FullManuscriptCreate, FullManuscriptResponse, FullManuscriptUpdate
from app.model import FullManuscript
from app.repository.manuscript_repo import ManuscriptRepository

class ManuscriptService:

    @staticmethod
    async def upload_manuscript(db: Session, manuscript_data: FullManuscriptCreate):
        _manuscript_id = str(uuid4())
        _manuscript_paper = FullManuscript(
            id = _manuscript_id,
            research_paper_id = manuscript_data.research_paper_id,
            content = manuscript_data.content,
            keywords = manuscript_data.keywords,
            file = manuscript_data.file,
            status = manuscript_data.status,
        )

        await ManuscriptRepository.create(db, **_manuscript_paper.dict())

    @staticmethod
    async def get_manuscript_by_research_paper_id(
        db: Session,
        research_paper_id: str
    ) -> Optional[FullManuscript]:
        research_paper = await ManuscriptRepository.get_by_research_paper_id(db, research_paper_id)
        
        if research_paper is None:
            raise HTTPException(status_code=404, detail="Full Manuscript not found")
        
        return research_paper
    

    @staticmethod
    async def update_manuscript(db: AsyncSession, manuscript_data: FullManuscriptUpdate, manuscript_id: str) -> FullManuscriptResponse:
        try:
            await ManuscriptRepository.update_manuscript(db, manuscript_id, **manuscript_data.dict())
            # Fetch the updated data from the database
            updated_manuscript = await ManuscriptRepository.get_manuscript_by_id(db, manuscript_id)
            return FullManuscriptResponse(**updated_manuscript.dict())
        except HTTPException:
            raise  # Re-raise the HTTPException
        except Exception as e:
            print(f"Error during update: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    @staticmethod
    async def delete_manuscript(db: Session, ethics_id: str):
        try:
            # Call the repository method to delete ethics data by ethics ID
            result = await ManuscriptRepository.delete_manuscript_id(db, ethics_id)

            if not result:
                raise HTTPException(status_code=404, detail="Ethics data not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
