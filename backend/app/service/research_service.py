from datetime import datetime
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.research_repo import ResearchPaperRepository
from app.schema import ResearchPaperCreate, ResearchPaperResponse
from app.service.users_service import UserService
from app.model import Users, ResearchPaper
from app.model.research_paper import Author, Status
from app.repository.author_repo import AuthorRepository
from app.model.research_status import Comment
from app.repository.comment_repo import CommentRepository

class ResearchService:

    @staticmethod
    async def create_research_paper(db: Session, research_paper_data: ResearchPaperCreate, author_ids: List[str]) -> ResearchPaper:
        _research_paper_id = str(uuid4())
        submitted_date = datetime.strptime(research_paper_data.submitted_date, '%d-%m-%Y')

        research_paper_data_dict = research_paper_data.dict()
        research_paper_data_dict.pop('submitted_date', None)

        research_paper = await ResearchPaperRepository.create(
            db,
            model=ResearchPaper,
            id=_research_paper_id,
            submitted_date=submitted_date,
            **research_paper_data_dict,
        )
        for author_id in author_ids:
            await AuthorRepository.create_author(db, author_id, _research_paper_id)
        return research_paper

    @staticmethod
    async def get_research_paper(
        db: Session,
        research_paper_id: str
    ) -> Optional[ResearchPaper]:
        research_paper = await ResearchPaperRepository.get_by_id(db, research_paper_id)
        
        if research_paper is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        
        return research_paper
    
    @staticmethod
    async def update_research_paper(
        db: Session,
        research_paper: ResearchPaper,
        research_paper_data: dict
    ) -> None:
        # Check if 'submitted_date' is in the update data
        if 'submitted_date' in research_paper_data:
            # Convert the 'submitted_date' to the desired format
            research_paper_data['submitted_date'] = datetime.strptime(research_paper_data['submitted_date'], '%d-%m-%Y')

        await ResearchPaperRepository.update(db, research_paper, **research_paper_data)


    @staticmethod
    async def delete_research_paper(
        db: Session,
        research_paper: ResearchPaper
    ) -> None:
        await ResearchPaperRepository.delete(db, research_paper)


    @staticmethod
    async def get_all_research_papers(db: Session) -> List[ResearchPaper]:
        """
        Get all research papers from the database.
        """
        research_papers = await ResearchPaperRepository.get_all(db)
        return research_papers
    
    
    @staticmethod
    async def get_current_user_research_paper(
        db: Session,
        user_id: int
    ) -> Optional[ResearchPaper]:
        # Assuming you have a method to get the current user's research paper
        research_paper = await ResearchPaperRepository.get_current_user_research_paper(db, user_id)
        
        if research_paper is None:
            raise HTTPException(status_code=404, detail="Research paper not found for the current user")
        
        return research_paper
            

#=============================MGA POWER NG FACULTY ========================#


# research_service.py

    @staticmethod
    async def check_faculty_permission(research_paper_id: str, faculty_username: str) -> bool:
        return await ResearchPaperRepository.check_adviser_permission(db, research_paper_id, faculty_username)

    @staticmethod
    async def update_research_paper_status(db: Session, research_paper_id: str, new_status: Status) -> ResearchPaper:

        research_paper = await ResearchPaperRepository.update_status(db, research_paper_id, new_status)
        return research_paper



#============================ WILL PUT RESEARCH COMMENTS HERE ==================#
    
    @staticmethod
    async def post_comment(db: Session, user_id: str, research_id: str, text: str):
        _comment_id = str(uuid4())
        _comment = Comment(
            id=_comment_id,
            text=text,
            user_id=user_id,
            research_paper_id=research_id
            )

        return await CommentRepository.create(db, **_comment.dict())
    
