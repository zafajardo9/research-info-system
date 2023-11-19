from datetime import datetime
from sqlalchemy import join
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.research_repo import ResearchPaperRepository
from app.schema import ResearchPaperCreate, ResearchPaperResponse, ResearchPaperResponseOnly
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
    
    
    # @staticmethod
    # async def get_research_paper_by_user_id(db: Session, user_id: str) -> List[ResearchPaper]:
    #     # Join the Author and ResearchPaper tables and filter by user_id
    #     papers = db.query(ResearchPaper).join(Author).filter(Author.user_id == user_id).all()

    #     return papers
    

    @staticmethod
    async def get_research_papers_by_user_id(db: Session, user_id: str) -> List[ResearchPaperResponseOnly]:
        # Build the equivalent SQL query
        query = (
            select([
                ResearchPaper.id,
                ResearchPaper.title,
                ResearchPaper.content,
                ResearchPaper.abstract,
                ResearchPaper.research_type,
                ResearchPaper.submitted_date,
                ResearchPaper.status,
                ResearchPaper.keywords,
                ResearchPaper.file_path,
                ResearchPaper.research_adviser,
            ])
            .select_from(join(ResearchPaper, Author, ResearchPaper.id == Author.research_paper_id))
            .where(Author.user_id == user_id)
        )

        # Execute the query and return the results
        return (await db.execute(query)).mappings().all()


#=============================MGA POWER NG FACULTY ========================#


# research_service.py


    @staticmethod
    async def get_adviser_papers(db: Session, faculty: str) -> List[ResearchPaperResponse]:
        # Build the equivalent SQL query using SQLAlchemy ORM
        query = select(ResearchPaper).filter(ResearchPaper.research_adviser == faculty)

        # Execute the query and fetch the results
        result = await db.execute(query)

        # Fetch all the rows from the result
        papers = result.scalars().all()

        # Assuming ResearchPaperResponseOnly is a class representing the response structure
        # You might need to adjust this part based on your actual response structure
        return [ResearchPaperResponseOnly(
            modified_at=paper.modified_at,
            created_at=paper.created_at,
            id=paper.id,
            title=paper.title,
            content=paper.content,
            abstract=paper.abstract,
            research_type=paper.research_type,
            submitted_date=paper.submitted_date,
            status=paper.status,
            keywords=paper.keywords,
            file_path=paper.file_path,
            research_adviser=paper.research_adviser,
        ) for paper in papers]
    



    @staticmethod
    async def check_if_faculty(current_user_role: str) -> bool:
        # Check if the user's role is 'faculty'
        if current_user_role != 'faculty':
            return False
        return True

    @staticmethod
    async def check_faculty_permission(research_paper_id: str, current_user_role: str) -> bool:
        # Check if the user's role is 'faculty'
        if current_user_role != 'faculty':
            return False
        return True
    

    @staticmethod
    async def update_research_paper_status(db: Session, research_paper_id: str, new_status: Status) -> ResearchPaper:

        research_paper = await ResearchPaperRepository.update_status(db, research_paper_id, new_status)
        return research_paper





#============================ WILL PUT RESEARCH COMMENTS HERE ==================#
    
    @staticmethod
    async def post_comment(db: Session, user_id: str, user_name: str, research_id: str, text: str):
        _comment_id = str(uuid4())
        _comment = Comment(
            id=_comment_id,
            text=text,
            name=user_name,
            user_id=user_id,
            research_paper_id=research_id
            )

        return await CommentRepository.create(db, **_comment.dict())
    
