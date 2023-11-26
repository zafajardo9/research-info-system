from datetime import datetime
from sqlalchemy import join
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.research_repo import ResearchPaperRepository
from app.schema import AuthorShow, CopyRightResponse, DisplayAllByUser, EthicsResponse, FullManuscriptResponse, ResearchPaperCreate, ResearchPaperResponse, ResearchPaperShow, ResearchPaperWithAuthorsResponse
from app.service.users_service import UserService
from app.model import Users, ResearchPaper, Ethics, FullManuscript, CopyRight, Student
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
        research_paper_data['status'] = 'Revised'
        await ResearchPaperRepository.update(db, research_paper, **research_paper_data)


    @staticmethod
    async def delete_research_paper(
        db: Session,
        research_paper: ResearchPaper
    ) -> None:
        await ResearchPaperRepository.delete(db, research_paper)



    @staticmethod
    async def get_research_paper_with_authors(db: Session, research_paper_id: str):
        query = (
            select(Users, ResearchPaper, Author, Student)
            .join(Author, Users.id == Author.user_id)
            .join(ResearchPaper, ResearchPaper.id == Author.research_paper_id)
            .join(Student, Users.student_id == Student.id)
            .where(ResearchPaper.id == research_paper_id)
        )

        # Execute the query and fetch all results
        result = await db.execute(query)
        query_result = result.fetchall()

        # Assuming you have a function to map the result to the desired response model
        response = ResearchService.map_to_response_model(query_result)
        return response
    

    @staticmethod
    def map_to_response_model(query_result):
    # Assuming a basic mapping, modify based on your actual data structure

        if not query_result:
            return None # Handle the case where no data is found

        user, research_paper, author, student = query_result[0]

        # Map research paper details
        research_paper_data = ResearchPaperShow(
            id=str(research_paper.id),
            title=str(research_paper.title),
            research_type=str(research_paper.research_type),
            submitted_date=str(research_paper.submitted_date),
            status=str(research_paper.status),
            file_path=str(research_paper.file_path),
            research_adviser=str(research_paper.research_adviser)
        )

        # Map authors
        authors_data = [
            AuthorShow(
                user_id=str(author.user_id),
                student_name=str(student.name),
                student_year=str(student.year),
                student_section=str(student.section),
                student_course=str(student.course),
                student_number=str(student.student_number),
                student_phone_number=str(student.phone_number)
            )
            for _, _, author, student in query_result
        ]

        # Create the response model
        response_model = ResearchPaperWithAuthorsResponse(
            research_paper=research_paper_data,
            authors=authors_data
        )

        return response_model


    

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
    async def get_research_papers_by_user(db: Session, user_id: str) -> List[ResearchPaper]:
        query = (
            select(ResearchPaper)
            .join(Author, ResearchPaper.id == Author.research_paper_id)
            .where(Author.user_id == user_id)
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


# research_service.py


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
    
