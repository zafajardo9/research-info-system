from datetime import datetime
import math
from operator import and_
from typing import List, Optional
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import case, desc, distinct, func, join, select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db
from app.model.research_paper import Author, FacultyResearchPaper, ResearchPaper, Status
from app.repository.base_repo import BaseRepo
from app.schema import AuthorShow, ChangeFacultyPaperStatus, DisplayAllByUser, MakeExtension, PageResponse, ResearchPaperCreate, ResearchPaperShow, ResearchPaperWithAuthorsResponse
from sqlalchemy.orm import joinedload
from app.model.users import Users
from app.model.research_status import Comment
from app.model.ethics import Ethics
from app.model.full_manuscript import FullManuscript
from app.model.copyright import CopyRight
from app.model.connected_SPS import SPSClass, SPSCourse, SPSCourseEnrolled, SPSMetadata, SPSStudentClassGrade
from app.model.student import Student
from app.model import ResearchDefense
from app.model.faculty import Faculty


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
            print(f"IntegrityError: {str(e)}")
            await commit_rollback()
        except Exception as e:
            print(f"Error deleting research paper: {str(e)}")
            # Rollback the changes on any error
            await commit_rollback()
            # Raise or return an appropriate response
            raise HTTPException(status_code=500, detail="Error deleting research paper")
                


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
            await db.commit()
            await db.refresh(research_paper)
            return research_paper
        else:
            raise HTTPException(status_code=404, detail="Research paper not found")



    @staticmethod
    async def faculty_paper_approve(db: Session, research_id: str, status: ChangeFacultyPaperStatus) -> ResearchPaper:
        # Fetch the research paper
        result = await db.execute(select(FacultyResearchPaper).where(FacultyResearchPaper.id == research_id))
        research_paper = result.scalar_one_or_none()

        if research_paper:
            # Assign values from make_extension
            research_paper.status = status.status
            await db.commit()
            await db.refresh(research_paper)
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
        if user_type is None and type_paper is None:
            
            return await ResearchPaperRepository.combine_faculty_student_papers()
        
        if user_type == "faculty":
            return await ResearchPaperRepository.get_faculty_papers()
            
        else:
            return await ResearchPaperRepository.get_student_papers_by_course(user_type, type_paper)
                
    
    
    @staticmethod
    async def combine_faculty_student_papers():
        faculty_papers = await ResearchPaperRepository.get_faculty_papers()
        student_papers = await ResearchPaperRepository.get_student_papers_all()

        combined_result = faculty_papers + student_papers

        return combined_result
    
    @staticmethod
    async def get_faculty_papers():
        query = (
            select(
                    FacultyResearchPaper.title,
                    FacultyResearchPaper.content,
                    FacultyResearchPaper.abstract,
                    FacultyResearchPaper.date_publish,
                    FacultyResearchPaper.keywords,
                    # FacultyResearchPaper.publisher,
                    # FacultyResearchPaper.category,
                    FacultyResearchPaper.file_path.label('file'),
                    func.concat(Faculty.LastName , ', ', Faculty.FirstName, ' ', Faculty.MiddleName).label('author'),
                )
                .join(Users, FacultyResearchPaper.user_id == Users.id)
                .join(Faculty, Users.faculty_id == Faculty.FacultyId)
        )
        result = await db.execute(query)
        overall_result = result.fetchall()

        faculty_response_list = []

        for research_paper in overall_result:
            faculty_paper_response = {
                "research_paper": {
                    "title": research_paper.title,
                    "content": research_paper.content,
                    "abstract": research_paper.abstract,
                    "keywords": research_paper.keywords,
                    "file": research_paper.file,
                    "date_publish": research_paper.date_publish,
                    "authors": [{"name": research_paper.author}],
                },
            }

            faculty_response_list.append(faculty_paper_response)

        return faculty_response_list
    
    
    @staticmethod
    async def get_student_papers_by_course(user_type: str, type_paper: str):
            research_paper_query = (
                select(
                    ResearchPaper.id,
                    ResearchPaper.title,
                    ResearchPaper.research_type,
                    FullManuscript.content,
                    FullManuscript.abstract,
                    FullManuscript.keywords,
                    FullManuscript.file.label('file'),
                    func.date(FullManuscript.modified_at).label('date_publish')
                )
                .distinct(ResearchPaper.title)  # Use distinct() method here
                .select_from(
                    join(ResearchPaper, FullManuscript, ResearchPaper.id == FullManuscript.research_paper_id)
                    .join(Author, ResearchPaper.id == FullManuscript.research_paper_id)

                )
                # .where(SPSCourse.CourseCode == user_type)
            )

            if type_paper:
                research_paper_query = research_paper_query.where(ResearchPaper.research_type == type_paper)

            research_paper_result = await db.execute(research_paper_query)
            paper_result = research_paper_result.fetchall()

            research_papers_list = []
            for research_paper in paper_result:
                authors_query = (
                    select(
                        Users.id.label('id'),
                        func.concat(Student.FirstName, ' ', Student.MiddleName, ' ', Student.LastName).label('name'),
                        # Student.StudentNumber.label('student_number'),
                        SPSCourse.CourseCode.label('course'),
                        # case([(SPSCourseEnrolled.Status == 1, 'Alumni')], else_='Student').label('status'),
                        # func.concat(SPSMetadata.Year, '-', SPSClass.Section).label('year_section'),
                    )
                    .distinct(Users.id)
                    .select_from(Users)
                    .join(Author, Users.id == Author.user_id)
                    .join(ResearchPaper, ResearchPaper.id == Author.research_paper_id)
                    .join(Student, Student.StudentId == Users.student_id)
                    .join(SPSCourseEnrolled, SPSCourseEnrolled.StudentId == Student.StudentId)
                    .join(SPSCourse, SPSCourse.CourseId == SPSCourseEnrolled.CourseId)
                    .join(SPSStudentClassGrade, SPSStudentClassGrade.StudentId == Student.StudentId)
                    .join(SPSClass, SPSClass.ClassId == SPSStudentClassGrade.ClassId)
                    .join(SPSMetadata, SPSMetadata.MetadataId == SPSClass.MetadataId)
                    .order_by(Users.id, desc(SPSMetadata.Year), SPSClass.Section)
                    .where(and_(ResearchPaper.id == research_paper.id, SPSCourse.CourseCode == user_type))
                )

                authors_result = await db.execute(authors_query)
                authors_details = authors_result.fetchall()
                authors_names = [{"name": author["name"]} for author in authors_details]


                # Check if there are authors with the specified user_type
                if any(author['course'] == user_type for author in authors_details):
                    # Create a dictionary for each research paper with its authors
                    result_dict = {
                        "research_paper": {
                            "title": research_paper.title,
                            #"research-type": research_paper.research_type,
                            "content": research_paper.content,
                            "abstract": research_paper.abstract,
                            "keywords": research_paper.keywords,
                            "file": research_paper.file,
                            "date_publish": research_paper.date_publish,
                            "authors": authors_names,
                        },
                    }

                    research_papers_list.append(result_dict)

            return research_papers_list
        
        
    @staticmethod
    async def get_student_papers_all():
        research_paper_query = (
            select(
                ResearchPaper.id,
                ResearchPaper.title,
                ResearchPaper.research_type,
                FullManuscript.content,
                FullManuscript.abstract,
                FullManuscript.keywords,
                FullManuscript.file,
                func.date(FullManuscript.modified_at).label('date_publish')
            )
            .distinct(ResearchPaper.title)  # Use distinct() method here
            .select_from(
                join(ResearchPaper, FullManuscript, ResearchPaper.id == FullManuscript.research_paper_id)
                .join(Author, ResearchPaper.id == FullManuscript.research_paper_id)
            )
        )

        research_paper_result = await db.execute(research_paper_query)
        paper_result = research_paper_result.fetchall()

        research_papers_list = []
        for research_paper in paper_result:
            authors_query = (
                select(
                    Users.id.label('id'),
                    func.concat(Student.FirstName, ' ', Student.MiddleName, ' ', Student.LastName).label('name'),
                )
                .distinct(Users.id)
                .select_from(Users)
                .join(Author, Users.id == Author.user_id)
                .join(ResearchPaper, ResearchPaper.id == Author.research_paper_id)
                .join(Student, Student.StudentId == Users.student_id)
                .order_by(Users.id)
                .where(ResearchPaper.id == research_paper.id)
            )

            authors_result = await db.execute(authors_query)
            authors_details = authors_result.fetchall()
            authors_names = [{"name": author["name"]} for author in authors_details]

            # Create a dictionary for each research paper with its authors
            result_dict = {
                "research_paper": {
                    "title": research_paper.title,
                    "content": research_paper.content,
                    "abstract": research_paper.abstract,
                    "keywords": research_paper.keywords,
                    "file": research_paper.file,
                    "date_publish": research_paper.date_publish,
                    "authors": authors_names,
                },
            }

            research_papers_list.append(result_dict)

        return research_papers_list