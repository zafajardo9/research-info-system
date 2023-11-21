from datetime import datetime
import math
from typing import List, Optional
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db
from app.model.research_paper import Author, ResearchPaper, Status
from app.repository.base_repo import BaseRepo
from app.schema import PageResponse, ResearchPaperCreate, ResearchPaperWithAuthorsResponse
from sqlalchemy.orm import joinedload
from app.model.users import Users
from app.model.research_status import Comment


class ResearchPaperRepository(BaseRepo):
    model = ResearchPaper


    @staticmethod
    async def get_by_id(db: Session, research_paper_id: str) -> ResearchPaper:
        query = select(ResearchPaper).where(ResearchPaper.id == research_paper_id)
        return (await db.execute(query)).scalar_one_or_none()
    

    @staticmethod
    async def get_all(db: Session) -> List[ResearchPaper]:
        """
        Get all research papers from the database.
        """
        query = select(ResearchPaper)
        return (await db.execute(query)).scalars().all()
    
    @staticmethod
    async def delete(research_id: str, db: Session):
        """ delete research data by id """

        # Delete related records in the Author table first
        await db.execute(delete(Author).where(Author.research_paper_id == research_id))

        # Delete related records in the Comments table
        await db.execute(delete(Comment).where(Comment.research_paper_id == research_id))

        # Now, delete the research paper
        query = delete(ResearchPaper).where(ResearchPaper.id == research_id)
        await db.execute(query)
        await commit_rollback()
                


    @staticmethod
    async def get_current_user_research_paper(db: Session, user_id: int) -> Optional[ResearchPaper]:
        # Assuming there is a relationship between Users and ResearchPaper through the Author model

        # Query to get the research paper for the current user
        query = (
            select(ResearchPaper)
            .join(Author)
            .join(Users)
            .filter(Users.id == user_id)
        )

        # Execute the query and return the result
        result = await db.execute(query)
        research_paper = result.scalar().all()

        return research_paper
    

    @staticmethod
    async def update_status(db: Session, research_paper_id: str, new_status: Status) -> ResearchPaper:
        # Fetch the research paper
        result = await db.execute(select(ResearchPaper).where(ResearchPaper.id == research_paper_id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            research_paper.status = new_status
            await db.commit()
            db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Research paper not found")
        


    # @staticmethod
    # async def get_research_paper_with_authors(db: Session, research_paper_id: str) -> ResearchPaperWithAuthorsResponse:
    #     research_paper = await db.execute(
    #         select(ResearchPaper)
    #         .options(joinedload(ResearchPaper.authors).joinedload(Author.user))
    #         .where(ResearchPaper.id == research_paper_id)
    #     )
    #     research_paper = research_paper.unique().one()

    #     # Convert the SQLAlchemy model instance to a dictionary
    #     research_paper_dict = research_paper.__dict__

    #     # Remove SQLAlchemy-specific attributes
    #     research_paper_dict = {k: v for k, v in research_paper_dict.items() if k in ResearchPaperWithAuthorsResponse.__fields__}

    #     # Convert the authors to a list of dictionaries
    #     research_paper_dict["authors"] = [
    #         {
    #             "id": author.id,
    #             "user_id": author.user_id,
    #             "research_paper_id": author.research_paper_id,
    #         }
    #         for author in research_paper.authors
    #     ]

    #     # Create a ResearchPaperWithAuthorsResponse from the dictionary
    #     return ResearchPaperWithAuthorsResponse(**research_paper_dict)