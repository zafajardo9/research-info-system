from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.research_repo import ResearchPaperRepository
from app.schema import ResearchPaperCreate
from app.service.users_service import UserService
from app.model import Users, ResearchPaper

class ResearchService:

    @staticmethod
    async def create_research_paper(
        db: Session, 
        research_paper_data: ResearchPaperCreate, 
        username: str
    ):
        _research_id = str(uuid4())
        
        #asdf asdf
        _research_paper = await ResearchPaperRepository.create(
            db, 
            id=_research_id,
            title=research_paper_data.title,
            content=research_paper_data.content,
            abstract=research_paper_data.abstract,
            research_type=research_paper_data.research_type,
            submitted_date=research_paper_data.submitted_date,
            keywords=research_paper_data.keywords,
            file_path=research_paper_data.file_path,
            research_adviser=research_paper_data.research_adviser,
            author_id=research_paper_data.author_id
        )
        
        return _research_paper
    

    @staticmethod
    async def get_research_paper(
        db: Session,
        research_paper_id: int
    ) -> Optional[ResearchPaper]:
        research_paper = await ResearchPaperRepository.get_by_id(db, research_paper_id)
        
        if research_paper is None:
            return None
        
        return research_paper
    
    @staticmethod
    async def update_research_paper(
        db: Session,
        research_paper: ResearchPaper,
        research_paper_data: dict
    ) -> None:
        await ResearchPaperRepository.update(db, research_paper, **research_paper_data)

    @staticmethod
    async def delete_research_paper(
        db: Session,
        research_paper: ResearchPaper
    ) -> None:
        await ResearchPaperRepository.delete(db, research_paper)