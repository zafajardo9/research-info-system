
from uuid import uuid4

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.model import Users, ResearchPaper
from app.repository.comment_repo import CommentRepository

class CommentService:
    pass
    
    # @staticmethod
    # async def delete_comment(
    #     db: Session,
    #     research_paper: ResearchPaper
    # ) -> None:
    #     await CommentRepository.delete(db, research_paper)

