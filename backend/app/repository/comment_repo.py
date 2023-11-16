from datetime import datetime
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db
from app.model.research_status import Comment
from app.repository.base_repo import BaseRepo


class CommentRepository(BaseRepo):
    model = Comment

    @staticmethod
    async def delete(comment_id: str):
        """ delete research data by id """
        try:
            query = delete(Comment).where(Comment.id == comment_id)
            await db.execute(query)
            await commit_rollback()
        except Exception as e:
            raise Exception(f"Error deleting comment: {str(e)}")
    
    @staticmethod
    async def get_comments_by_research_id(research_paper_id: str):
        """ get all comments by research id """
        try:
            query = select(Comment).where(Comment.research_paper_id == research_paper_id)
            result = await db.execute(query)
            comments = result.scalars().all()
            return comments
        except Exception as e:
            raise Exception(f"Error getting comments: {str(e)}")