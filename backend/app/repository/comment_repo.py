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