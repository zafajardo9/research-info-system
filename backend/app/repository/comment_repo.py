from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db
from app.model.research_status import Comment
from app.repository.base_repo import BaseRepo
from app.model.users import Users
from typing import List, Dict



class CommentRepository(BaseRepo):
    model = Comment

    @staticmethod
    async def delete(db: Session, comment_id: str):
        """ delete research data by id """
        try:
            query = delete(Comment).where(Comment.id == comment_id)
            await db.execute(query)
            await commit_rollback()
        except Exception as e:
            raise Exception(f"Error deleting comment: {str(e)}")
        
    
    # @staticmethod
    # async def get_comments_by_research_id_with_user_details(db: Session, research_id: str) -> List[Dict]:
    #     """ get all comments by research id with user details """
    #     try:
    #         query = (
    #             select(Comment, Users.username)
    #             .join(Users, Comment.user_id == Users.id)
    #             .where(Comment.research_paper_id == research_id)
    #         )

    #         # Ensure that the database session is an asynchronous session
    #         result = await db.execute(query)

    #         # Fetch the results asynchronously
    #         result = await result.all()

    #         # Check if any results were found
    #         if not result:
    #             raise HTTPException(status_code=404, detail="No comments found for the given research_id")

    #         # Process the results to extract relevant information
    #         comments_with_username = [{"comment": comment, "username": username} for comment, username in result]

    #         return {"comments_with_username": comments_with_username}

    #     except Exception as e:
    #         # Log the unexpected error for debugging purposes
    #         print(f"Unexpected error during database query: {str(e)}")
    #         raise HTTPException(status_code=500, detail="Internal Server Error")

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