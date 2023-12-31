from datetime import datetime
from sqlalchemy import delete, join, update
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.research_repo import ResearchPaperRepository
from app.schema import AuthorShow, CopyRightResponse, DisplayAllByUser, EthicsResponse, FacultyResearchPaperCreate, FacultyResearchPaperUpdate, FullManuscriptResponse, ResearchPaperCreate, ResearchPaperResponse, ResearchPaperShow, ResearchPaperWithAuthorsResponse
from app.service.users_service import UserService
from app.model import Users, ResearchPaper, Ethics, FullManuscript, CopyRight, Student
from app.model.research_paper import Author, FacultyResearchPaper, Status
from app.repository.author_repo import AuthorRepository
from app.model.research_status import Comment
from app.repository.comment_repo import CommentRepository
from app.repository.faculty_research_paper import FacultyResearchRepository
from app.model.faculty import Faculty
from app.model.student import Class

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
        research_paper_data['status'] = 'Revised'
        await ResearchPaperRepository.update(db, research_paper, **research_paper_data)


    @staticmethod
    async def delete_research_paper(
        db: Session,
        research_paper: ResearchPaper
    ) -> None:
        await ResearchPaperRepository.delete(db, research_paper)


    @staticmethod
    async def get_all_with_authors():
        try:
            # Query to get research paper details
            research_paper_query = select(ResearchPaper)
            research_paper_result = await db.execute(research_paper_query)
            research_papers = research_paper_result.scalars().all()

            # List to store all research papers with authors
            research_papers_with_authors = []

            for research_paper in research_papers:
                # Query to get authors' details for each research paper
                authors_query = (
                    select(Users.id, Student.name, Student.student_number, Class.section, Class.course)
                    .join(Author, Users.id == Author.user_id)
                    .join(ResearchPaper, ResearchPaper.id == Author.research_paper_id)
                    .join(Student, Users.student_id == Student.id)
                    .join(Class, Class.id == Student.class_id)
                    .where(ResearchPaper.id == research_paper.id)
                )

                authors_result = await db.execute(authors_query)
                authors_details = authors_result.fetchall()

                # Create a dictionary for each research paper with its authors
                result_dict = {
                    "research_paper": research_paper,
                    "authors": authors_details,
                }

                research_papers_with_authors.append(result_dict)

            return research_papers_with_authors

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    @staticmethod
    async def get_research_paper_with_authors(research_paper_id: str):
        try:
            research_paper_query = (select(
                                    ResearchPaper.id,
                                    ResearchPaper.title,
                                    ResearchPaper.submitted_date,
                                    ResearchPaper.status,
                                    ResearchPaper.research_type,
                                    ResearchPaper.file_path,
                                    ResearchPaper.research_adviser,
                                    Faculty.name.label("faculty_name")
                                )
                                .join(Users, ResearchPaper.research_adviser == Users.id)
                                .join(Faculty, Users.faculty_id == Faculty.id)
                                .where(ResearchPaper.id == research_paper_id)
                                )
            research_paper_result = await db.execute(research_paper_query)
            research_paper = research_paper_result.fetchall()
            print(research_paper)


            if not research_paper:
                raise HTTPException(status_code=404, detail=f"Research paper with id {research_paper_id} not found.")

            # Query to get authors' details
            authors_query = (
                select(Users.id, Student.name, Student.student_number, Class.section, Class.course)
                .join(Author, Users.id == Author.user_id)
                .join(ResearchPaper, ResearchPaper.id == Author.research_paper_id)
                .join(Student, Users.student_id == Student.id)
                .join(Class, Class.id == Student.class_id)
                .where(ResearchPaper.id == research_paper_id)
            )

            authors_result = await db.execute(authors_query)
            authors_details = authors_result.fetchall()
            


            # Create a dictionary to hold the results
            result_dict = {
                "research_paper": research_paper,
                "authors": authors_details,
            }

            return result_dict

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    @staticmethod
    async def show_paper_author_list(research_paper_id: str):
        try:

            authors_query = (
                select(Users.id, Student.name, Student.student_number, Class.section, Class.course)
                .join(Author, Users.id == Author.user_id)
                .join(ResearchPaper, ResearchPaper.id == Author.research_paper_id)
                .join(Student, Users.student_id == Student.id)
                .join(Class, Class.id == Student.class_id)
                .where(ResearchPaper.id == research_paper_id)
            )

            authors_result = await db.execute(authors_query)
            authors_details = authors_result.fetchall()
            

            result_dict = {
                "authors": authors_details,
            }

            return result_dict

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




    # @staticmethod
    # def map_to_response_model(query_result):

    #     if query_result is None or not query_result:
    #         return None

    #     user, research_paper, author, student = query_result[0]

    #     # Map research paper details
    #     research_paper_data = ResearchPaperShow(
    #         id=str(research_paper.id),
    #         title=str(research_paper.title),
    #         research_type=str(research_paper.research_type),
    #         submitted_date=str(research_paper.submitted_date),
    #         status=str(research_paper.status),
    #         file_path=str(research_paper.file_path),
    #         research_adviser=str(research_paper.research_adviser)
    #     )

    #     # Map authors
    #     authors_data = [
    #         AuthorShow(
    #             user_id=str(author.user_id),
    #             student_name=str(student.name),
    #             student_year=str(student.year),
    #             student_section=str(student.section),
    #             student_course=str(student.course),
    #             student_number=str(student.student_number),
    #             student_phone_number=str(student.phone_number)
    #         )
    #         for _, _, author, student in query_result
    #     ]
    #     if research_paper_data is None or authors_data is None:
    #         return None
    #     # Create the response model
    #     response_model = ResearchPaperWithAuthorsResponse(
    #         research_paper=research_paper_data,
    #         authors=authors_data
    #     )

    #     return response_model


    

    @staticmethod
    async def get_all_research_papers(db: Session) -> List[ResearchPaper]:
        """
        Get all research papers from the database.
        """
        research_papers = await ResearchPaperRepository.get_all(db)
        return research_papers
        
    @staticmethod
    async def get_research_papers_by_adviser(db: Session, user_id: str) -> List[ResearchPaper]:
        query = (
            select(ResearchPaper)
            .filter(ResearchPaper.research_adviser == user_id)
        )
        result = await db.execute(query)
        research_papers = result.scalars().all()

        return research_papers
    
    @staticmethod
    async def get_research_papers_by_user(user_id: str, research_type: str) -> List[ResearchPaper]:
        query = (
            select(ResearchPaper)
            .join(Author, ResearchPaper.id == Author.research_paper_id)
            .where((Author.user_id == user_id) & (ResearchPaper.research_type == research_type))
        )
        result = await db.execute(query)
        research_papers = result.scalars().all()

        return research_papers
    

    # @staticmethod
    # async def get_all_by_user(db: Session, user_id: str) -> List[DisplayAllByUser]:
    #     query = (
    #         select(ResearchPaper)
    #         .join(ResearchPaper.authors)
    #         .filter_by(user_id=user_id)
    #         .options(
    #             joinedload(ResearchPaper.ethics),
    #             joinedload(ResearchPaper.full_manuscript),
    #             joinedload(ResearchPaper.copyright),
    #         )
    #     )

    #     result = await db.execute(query)
    #     research_papers = result.scalars().all()

    #     display_result = []
    #     for research_paper in research_papers:
    #         display_result.append(
    #             DisplayAllByUser(
    #                 research_paper_id=research_paper.id,
    #                 title=research_paper.title,
    #                 research_type=research_paper.research_type,
    #                 submitted_date=str(research_paper.submitted_date),
    #                 status=research_paper.status,
    #                 file_path=research_paper.file_path,
    #                 research_adviser=research_paper.research_adviser,
    #                 ethics=research_paper.ethics,
    #                 full_manuscript=research_paper.full_manuscript,
    #                 copyright=research_paper.copyright,
    #             )
    #         )

    #     return display_result
    @staticmethod
    async def all_by_current_user(db: Session, user_id: str):
            # .join(Author, Users.id == Author.user_id)
            # .join(ResearchPaper, ResearchPaper.id == Author.research_paper_id)
            # .join(Student, Users.student_id == Student.id)
            # .where(ResearchPaper.id == research_paper_id)
        query = (
            select(ResearchPaper).
            # join(Author, ResearchPaper.authors).
            # join(Ethics, ResearchPaper.ethics).
            # join(FullManuscript, ResearchPaper.full_manuscript).
            # join(CopyRight, ResearchPaper.copyright).
            # join(Users, Author.user_id == Users.id).
            
            join(Author, Author.research_paper_id == ResearchPaper.id).
            join(Users, Users.id == Author.user_id).  # Add this join for the "users" table
            join(Ethics, Ethics.research_paper_id == ResearchPaper.id).
            join(FullManuscript, FullManuscript.research_paper_id == ResearchPaper.id).
            join(CopyRight, CopyRight.research_paper_id == ResearchPaper.id).
            join(Student, Users.student_id == Student.id).
            where(Author.id == user_id).
            options(
                contains_eager(ResearchPaper.authors),
                contains_eager(ResearchPaper.ethics),
                contains_eager(ResearchPaper.full_manuscript),
                contains_eager(ResearchPaper.copyright),
            )
        )
        # Execute the query and fetch all results
        result = await db.execute(query)
        query_result = result.scalars().all()

        # Assuming you have a function to map the result to the desired response model
        response = [ResearchService.map_for_all(r) for r in query_result]
        return response

    @staticmethod
    def map_for_all(query_result):
        if not query_result:
            return None

        user, research_paper, author, student, ethics, manuscript, copyright = query_result[0]

        research_paper_data = ResearchPaperShow(
            id=str(research_paper.id),
            title=str(research_paper.title),
            research_type=str(research_paper.research_type),
            submitted_date=str(research_paper.submitted_date),
            status=str(research_paper.status),
            file_path=str(research_paper.file_path),
            research_adviser=str(research_paper.research_adviser),
        )

        authors_data = [
            AuthorShow(
                user_id=str(author.user_id),
                student_name=str(student.name),
                student_year=str(student.year),
                student_section=str(student.section),
                student_course=str(student.course),
                student_number=str(student.student_number),
                student_phone_number=str(student.phone_number),
            )
            for _, _, author, student, _, _, _ in query_result
        ]

        # Assuming you have similar schema for Ethics, FullManuscript, and CopyRight
        ethics_data = EthicsResponse(
            id=str(ethics.id),
            modified_at=str(ethics.modified_at),
            created_at=str(ethics.created_at),
            letter_of_intent=str(ethics.letter_of_intent),
            urec_9=str(ethics.urec_9),
            urec_10=str(ethics.urec_10),
            urec_11=str(ethics.urec_11),
            urec_12=str(ethics.urec_12),
            certificate_of_validation=str(ethics.certificate_of_validation),
            co_authorship=str(ethics.co_authorship),
            research_paper_id=str(ethics.research_paper_id),
        )

        manuscript_data = FullManuscriptResponse(
            id=str(manuscript.id),
            modified_at=str(manuscript.modified_at),
            created_at=str(manuscript.created_at),
            research_paper_id=str(manuscript.research_paper_id),
            content=str(manuscript.content),
            keywords=str(manuscript.keywords),
            abstract=str(manuscript.abstract),
            file=str(manuscript.file),
            status=str(manuscript.status),
        )

        copyright_data = CopyRightResponse(
            id=str(copyright.id),
            modified_at=str(copyright.modified_at),
            created_at=str(copyright.created_at),
            research_paper_id=str(copyright.research_paper_id),
            co_authorship=str(copyright.co_authorship),
            affidavit_co_ownership=str(copyright.affidavit_co_ownership),
            joint_authorship=str(copyright.joint_authorship),
            approval_sheet=str(copyright.approval_sheet),
            receipt_payment=str(copyright.receipt_payment),
            recordal_slip=str(copyright.recordal_slip),
            acknowledgement_receipt=str(copyright.acknowledgement_receipt),
            certificate_copyright=str(copyright.certificate_copyright),
            recordal_template=str(copyright.recordal_template),
            ureb_18=str(copyright.ureb_18),
            journal_publication=str(copyright.journal_publication),
            copyright_manuscript=str(copyright.copyright_manuscript),
        )

        response_model = DisplayAllByUser(
            research_paper=research_paper_data,
            authors=authors_data,
            ethics=ethics_data,
            manuscript=manuscript_data,
            copyright=copyright_data,
        )

        return response_model




#=============================MGA POWER NG FACULTY ========================#


    @staticmethod
    async def get_research_ethics_by_adviser(db: Session, user_id: str) -> List[Ethics]:
        query = (
            select(ResearchPaper, Ethics)
            .join(Ethics, ResearchPaper.id == Ethics.research_paper_id)
            .filter(ResearchPaper.research_adviser == user_id)
        )
        result = await db.execute(query)
        research_papers = result.fetchall()

        return research_papers
    
    @staticmethod
    async def get_research_manuscript_by_adviser(db: Session, user_id: str) -> List[FullManuscript]:
        query = (
            select(ResearchPaper, FullManuscript)
            .join(FullManuscript, ResearchPaper.id == FullManuscript.research_paper_id)
            .filter(ResearchPaper.research_adviser == user_id)
        )
        result = await db.execute(query)
        research_papers = result.fetchall()

        return research_papers
    

    @staticmethod
    async def get_research_copyright_by_adviser(db: Session, user_id: str) -> List[CopyRight]:
        query = (
            select(ResearchPaper, CopyRight)
            .join(CopyRight, ResearchPaper.id == CopyRight.research_paper_id)
            .filter(ResearchPaper.research_adviser == user_id)
        )
        result = await db.execute(query)
        research_papers = result.fetchall()

        return research_papers

    @staticmethod
    async def check_if_faculty(current_user_role: str) -> bool:
        # Check if the user's role is 'faculty'
        if current_user_role != 'faculty':
            return False
        return True

    @staticmethod
    async def check_faculty_permission(current_user_role: str) -> bool:
        # Check if the user's role is 'faculty'
        if current_user_role != 'faculty':
            return False
        return True
    
    @staticmethod
    async def check_student_permission(current_user_role: str) -> bool:
        # Check if the user's role is 'faculty'
        if current_user_role != 'student':
            return False
        return True
    
    @staticmethod
    async def check_admin_permission(current_user_role: str) -> bool:
        # Check if the user's role is 'faculty'
        if current_user_role != 'admin':
            return False
        return True
    
    

    @staticmethod
    async def update_research_paper_status(db: Session, research_paper_id: str, new_status: Status) -> ResearchPaper:

        research_paper = await ResearchPaperRepository.update_status(db, research_paper_id, new_status)
        return research_paper
    
    # STATUS NG MGA PINAPASA RELATED SA PAPER
    @staticmethod
    async def update_ethics_status(db: Session, ethics_id: str, new_status: Status) -> ResearchPaper:

        ethics_paper = await ResearchPaperRepository.update_ethics_status(db, ethics_id, new_status)
        return ethics_paper
    

    @staticmethod
    async def update_manuscript_status(db: Session, manuscript_id: str, new_status: Status) -> ResearchPaper:

        manuscript_paper = await ResearchPaperRepository.update_manuscript_status(db, manuscript_id, new_status)
        return manuscript_paper
    
    @staticmethod
    async def update_copyright_status(db: Session, copyright_id: str, new_status: Status) -> ResearchPaper:

        copyright_paper = await ResearchPaperRepository.update_copyright_status(db, copyright_id, new_status)
        return copyright_paper





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
    




    @staticmethod
    async def upload_faculty_paper(user_id: str, research_paper_data: FacultyResearchPaperCreate) -> FacultyResearchPaper:
        _research_paper_id = str(uuid4())

        research_paper = await FacultyResearchRepository.create(
            db,
            model=FacultyResearchPaper,
            id=_research_paper_id,
            **research_paper_data.dict(),
            user_id=user_id,
        )
        return research_paper
    
    
    @staticmethod
    async def get_faculty_research_papers(user_id: str):
        query = select(FacultyResearchPaper).where(FacultyResearchPaper.user_id == user_id)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    
    @staticmethod
    async def get_faculty_research_papers_with_user_info():
        query = (
            select(FacultyResearchPaper, Faculty.name, Users.id, Users.email)
            .join(Users, FacultyResearchPaper.user_id == Users.id)
            .join(Faculty, Users.faculty_id == Faculty.id)
        )
        result = await db.execute(query)
        return result.fetchall()

    @staticmethod
    async def get_faculty_research_papers_by_id(faculty_paper_id: str):
        query = select(FacultyResearchPaper).where(FacultyResearchPaper.id == faculty_paper_id)
        
        result = await db.execute(query)
        return result.scalars().first()
    
    @staticmethod
    async def delete_faculty_research_paper(faculty_paper_id: str):
        query = delete(FacultyResearchPaper).where(FacultyResearchPaper.id == faculty_paper_id)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def update_faculty_research_paper(research_paper_id: str, research_paper_data: FacultyResearchPaperUpdate):
        query = update(FacultyResearchPaper).where(FacultyResearchPaper.id == research_paper_id).values(research_paper_data.dict())
        await db.execute(query)
        await db.commit()
