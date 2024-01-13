from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db
from app.model.research_status import Comment
from app.repository.base_repo import BaseRepo
from app.model.users import Users
from typing import List, Dict
from sqlalchemy.orm import joinedload

from app.schema import FacultyInfo, ResearchCommentResponse, StudentInfo
from app.model.faculty import Faculty
from app.model.student import Student


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
        

    @staticmethod
    async def get_comments_by_research_id(research_paper_id: str):
        try:
            # Join Users with Faculty and Student
            query = (
                select(Comment, Users,
                       func.concat(Student.FirstName, ' ', Student.MiddleName, ' ', Student.LastName).label('student_name'),
                       func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('faculty_name'))
                .join(Users, Comment.user_id == Users.id)
                .outerjoin(Student, Users.student_id == Student.StudentId)
                .outerjoin(Faculty, Users.faculty_id == Faculty.FacultyId)
                .options(joinedload(Users.faculty), joinedload(Users.student))
                .where(Comment.research_paper_id == research_paper_id)
            )

            result = await db.execute(query)
            comments_with_users = result.fetchall()

            comments = []
            for comment, user, student_name, faculty_name in comments_with_users:
                user_info = None

                if user.faculty:
                    user_info = FacultyInfo(name=faculty_name)
                elif user.student:
                    user_info = StudentInfo(name=student_name)

                # Add user info to the comment
                comment_dict = {
                    "id": comment.id,
                    "text": comment.text,
                    "created_at": comment.created_at,
                    "user_id": comment.user_id,
                    "research_paper_id": comment.research_paper_id,
                    "user_info": user_info,
                }
                comments.append(comment_dict)

            # Convert dictionaries to ResearchCommentResponse objects
            return [ResearchCommentResponse(**comment_dict) for comment_dict in comments]

        except Exception as e:
            raise Exception(f"Error getting comments: {str(e)}")