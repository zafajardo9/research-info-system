from datetime import datetime
from sqlalchemy import join
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException



from app.schema import EthicsCreate, EthicsResponse, EthicsUpdate
from app.service.users_service import UserService
from app.model import Ethics
from app.repository.ethics_repo import EthicsRepository
from app.model.research_paper import Author, ResearchPaper, Status
from app.model import FullManuscript, CopyRight

class EthicsService:
    
    @staticmethod
    async def upload_ethics(db: Session, ethics_data: EthicsCreate):
        _ethics_id = str(uuid4())
        _research_paper = Ethics(
            id = _ethics_id,
            research_paper_id = ethics_data.research_paper_id,
            letter_of_intent = ethics_data.letter_of_intent,
            urec_9 = ethics_data.urec_9,
            urec_10 = ethics_data.urec_10,
            urec_11 = ethics_data.urec_11,
            urec_12 = ethics_data.urec_12,
            certificate_of_validation = ethics_data.certificate_of_validation,
            co_authorship = ethics_data.co_authorship,
            workflow_step_id=ethics_data.workflow_step_id
        )

        await EthicsRepository.create(db, **_research_paper.dict())


    @staticmethod
    async def get_ethics_by_research_paper_id(
        db: Session,
        research_paper_id: str
    ) -> Optional[Ethics]:
        research_paper = await EthicsRepository.get_by_research_paper_id(db, research_paper_id)
        
        if research_paper is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        
        return research_paper

    @staticmethod
    async def update_ethics(db: AsyncSession, ethics_data: EthicsUpdate, ethics_id: str) -> EthicsResponse:
        try:
            await EthicsRepository.update_ethics(db, ethics_id, **ethics_data.dict())
            # Fetch the updated data from the database
            updated_ethics = await EthicsRepository.get_ethics_by_id(db, ethics_id)
            return EthicsResponse(**updated_ethics.dict())
        except HTTPException:
            raise  # Re-raise the HTTPException
        except Exception as e:
            print(f"Error during update: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    @staticmethod
    async def update_ethics_status(db: Session, id: str, new_status: Status) -> Ethics:

        research_paper = await EthicsRepository.update_status(db, id, new_status)
        return research_paper
    
    @staticmethod
    async def update_copyright_status(db: Session, id: str, new_status: Status) -> CopyRight:

        research_paper = await EthicsRepository.update_status_copy(db, id, new_status)
        return research_paper
    
    
    @staticmethod
    async def update_manuscript_status(db: Session, id: str, new_status: Status) -> FullManuscript:

        research_paper = await EthicsRepository.update_status_manu(db, id, new_status)
        return research_paper
    
    


    @staticmethod
    async def delete_ethics(db: Session, ethics_id: str):
        try:
            # Call the repository method to delete ethics data by ethics ID
            result = await EthicsRepository.delete_by_ethics_id(db, ethics_id)

            if not result:
                raise HTTPException(status_code=404, detail="Ethics data not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    @staticmethod
    async def get_ethics_by_user(db: Session, user_id: str) -> List[Ethics]:
        query = (
            select(Ethics)
            .join(ResearchPaper, Ethics.research_paper_id == ResearchPaper.id)
            .join(Author, ResearchPaper.id == Author.research_paper_id)
            .where(Author.user_id == user_id)
        )
        result = await db.execute(query)
        ethics_list = result.scalars().all()

        if not ethics_list:
            raise HTTPException(status_code=404, detail="Ethics data not found for the user")

        return ethics_list
