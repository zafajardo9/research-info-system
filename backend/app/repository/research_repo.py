from datetime import datetime
import math
from typing import List, Optional
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import distinct, join, select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db
from app.model.research_paper import Author, FacultyResearchPaper, ResearchPaper, Status
from app.repository.base_repo import BaseRepo
from app.schema import AuthorShow, DisplayAllByUser, MakeExtension, PageResponse, ResearchPaperCreate, ResearchPaperShow, ResearchPaperWithAuthorsResponse
from sqlalchemy.orm import joinedload
from app.model.users import Users
from app.model.research_status import Comment
from app.model.ethics import Ethics
from app.model.full_manuscript import FullManuscript
from app.model.copyright import CopyRight
from app.model.connected_SPS import SPSCourse, SPSCourseEnrolled
from app.model.student import Student
from app.model import ResearchDefense


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

        try:
            # Delete records from related tables
            await db.execute(delete(Author).where(Author.research_paper_id == research_id))
            await db.execute(delete(Comment).where(Comment.research_paper_id == research_id))
            await db.execute(delete(ResearchDefense).where(ResearchDefense.research_paper_id == research_id))
            await db.execute(delete(Ethics).where(Ethics.research_paper_id == research_id))
            await db.execute(delete(FullManuscript).where(FullManuscript.research_paper_id == research_id))
            await db.execute(delete(CopyRight).where(CopyRight.research_paper_id == research_id))

            # Now, delete the research paper
            query = delete(ResearchPaper).where(ResearchPaper.id == research_id)
            await db.execute(query)

            # Commit the changes
            await commit_rollback()

        except IntegrityError as e:
            # Handle any integrity errors, such as foreign key constraints
            # You can log the error or take appropriate action based on your requirements
            print(f"IntegrityError: {str(e)}")
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
        
    # ========================== DITO MGA STATUSES ======================
    @staticmethod
    async def update_ethics_status(db: Session, id: str, new_status: Status) -> ResearchPaper:
        # Fetch the research paper
        result = await db.execute(select(Ethics).where(Ethics.id == id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            research_paper.status = new_status
            await db.commit()
            db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Research paper not found")
        
    @staticmethod
    async def update_manuscript_status(db: Session, id: str, new_status: Status) -> ResearchPaper:
        # Fetch the research paper
        result = await db.execute(select(FullManuscript).where(FullManuscript.id == id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            research_paper.status = new_status
            await db.commit()
            db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Research paper not found")
        

    @staticmethod
    async def update_copyright_status(db: Session, id: str, new_status: Status) -> ResearchPaper:
        # Fetch the research paper
        result = await db.execute(select(CopyRight).where(CopyRight.id == id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            research_paper.status = new_status
            await db.commit()
            db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Research paper not found")
        


    @staticmethod
    async def make_paper_extension(db: Session, research_id: str, make_extension: MakeExtension) -> ResearchPaper:
        # Fetch the research paper
        result = await db.execute(select(ResearchPaper).where(ResearchPaper.id == research_id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            # Assign values from make_extension
            research_paper.extension = make_extension.extension
            research_paper.extension_type = make_extension.extension_type
            await db.commit()
            db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Research paper not found")


    @staticmethod
    def map_to_research_paper_model(query_result):
        # Map research paper details
        user, research_paper, _, _ = query_result
        return ResearchPaperShow(
            id=str(research_paper.id),
            title=str(research_paper.title),
            research_type=str(research_paper.research_type),
            submitted_date=str(research_paper.submitted_date),
            status=str(research_paper.status),
            file_path=str(research_paper.file_path),
            research_adviser=str(research_paper.research_adviser)
        )

    @staticmethod
    def map_to_author_model(query_result):
        # Map authors
        _, _, author, student = query_result
        return AuthorShow(
            user_id=str(author.user_id),
            student_name=str(student.name),
            student_year=str(student.year),
            student_section=str(student.section),
            student_course=str(student.course),
            student_number=str(student.student_number),
            student_phone_number=str(student.phone_number)
        )
        
        
        
    @staticmethod
    async def pagination_all_papers(user_type: str, type_paper: str = None):
        
        if user_type == "faculty":
            research_paper_query = select(
                FacultyResearchPaper.title,
                FacultyResearchPaper.content,
                FacultyResearchPaper.abstract,
                FacultyResearchPaper.file_path,
                FacultyResearchPaper.date_publish,
                #FacultyResearchPaper.category
                )
            research_paper_result = await db.execute(research_paper_query)
            return research_paper_result.fetchall()
            
        else:
            research_paper_query = (
            select(
                distinct(ResearchPaper.title).label('title'),
                FullManuscript.content,
                FullManuscript.abstract,
                FullManuscript.file.label('file_path'),
                FullManuscript.modified_at.label('date_publish')
            )
            .select_from(
                join(ResearchPaper, FullManuscript, ResearchPaper.id == FullManuscript.research_paper_id)
                .join(Author, ResearchPaper.id == FullManuscript.research_paper_id)
                .join(Users, Author.user_id == Users.id)
                .join(Student, Users.student_id == Student.StudentId)
                .join(SPSCourseEnrolled, Student.StudentId == SPSCourseEnrolled.StudentId)
                .join(SPSCourse, SPSCourseEnrolled.CourseId == SPSCourse.CourseId)
            )
            .where(SPSCourse.CourseCode == user_type)
            )
            if type_paper:
                research_paper_query = research_paper_query.where(ResearchPaper.research_type == type_paper)

            research_paper_result = await db.execute(research_paper_query)
            return research_paper_result.fetchall()
    
    
    
