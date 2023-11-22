from datetime import datetime
from sqlalchemy import join
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException



from app.schema import EthicsCreate, EthicsResponse
from app.service.users_service import UserService
from app.model import Ethics
from app.repository.author_repo import AuthorRepository
from app.model.research_status import Comment
from app.repository.comment_repo import CommentRepository
from app.repository.ethics_repo import EthicsRepository

class EthicsService:
    
    @staticmethod
    async def upload_ethics(db: Session, ethics_data: EthicsCreate, research_paper_id: str):
        _ethics_id = str(uuid4())
        _research_paper = Ethics(
            id = _ethics_id,
            research_paper_id = research_paper_id,
            letter_of_intent = ethics_data.letter_of_intent,
            urec_9 = ethics_data.urec_9,
            urec_10 = ethics_data.urec_10,
            urec_11 = ethics_data.urec_11,
            urec_12 = ethics_data.urec_12,
            certificate_of_validation = ethics_data.certificate_of_validation,
            co_authorship = ethics_data.co_authorship,
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
    async def update_ethics(db: Session, ethics_data: EthicsCreate, research_paper_id: str) -> EthicsResponse:
        try:
            existing_ethics = await EthicsRepository.get_by_research_paper_id(db, research_paper_id)

            if existing_ethics is not None:
                # Update the existing ethics data
                for key, value in ethics_data.dict().items():
                    setattr(existing_ethics, key, value)

                # Commit the changes to the database
                await db.commit()

                return EthicsResponse(**existing_ethics.dict())
            else:
                raise HTTPException(status_code=404, detail="Ethics data not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    @staticmethod
    async def delete_ethics(db: Session, ethics_id: str):
        try:
            # Call the repository method to delete ethics data by ethics ID
            result = await EthicsRepository.delete_by_ethics_id(db, ethics_id)

            if not result:
                raise HTTPException(status_code=404, detail="Ethics data not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
