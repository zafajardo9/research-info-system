from typing import List
from uuid import uuid4
from sqlalchemy import func, select

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.repository.author_repo import AuthorRepository
from app.schema import AuthorSchema
from app.model import Users, Author
from app.model.research_paper import Status

from app.model import ResearchPaper, Ethics, FullManuscript, CopyRight, Student, Faculty

class AllInformationService:

    # ALL ABOUT USER IN THE SYSTEM ========================
    @staticmethod
    async def get_student_count_all(db: Session):
        query = f"SELECT COUNT(*) FROM student;"
        result = await db.execute(query)
        count = result.scalar()
        return count

    @staticmethod
    async def get_student_count_by_course(db: Session, course: str):
        query = f"SELECT COUNT(*) FROM student WHERE course = '{course}';"
        result = await db.execute(query)
        count = result.scalar()
        return count
    
    @staticmethod
    async def read_student_count_by_course_section(db: Session, course: str, section: str):
        query = f"SELECT COUNT(*) FROM student WHERE course = '{course}' AND section = '{section}';"
        result = await db.execute(query)
        count = result.scalar()
        return count
    
    
    # ALL ABOUT RESEARCH ================================
    @staticmethod
    async def get_number_of_research_by_type(db: Session):
        types = ["Research", "Capstone", "Business Plan", "Feasibility Study"]
        counts = {}

        for research_type in types:
            query = f"SELECT COUNT(*) FROM research_papers WHERE research_type = '{research_type}';"
            result = await db.execute(query)
            count = result.scalar()
            counts[research_type] = count

        return {
            "Research": "Number of Research based on type",
            "Counts": counts
        }


    @staticmethod
    async def get_number_of_research_proposal(db: Session):
        query = f"SELECT COUNT(*) FROM research_papers;"
        result = await db.execute(query)
        count = result.scalar()
        return count
    


    @staticmethod
    async def get_number_of_research_proposal_by_status(db: Session, status: Status):
        if status not in [Status.Approved, Status.Rejected, Status.Pending, Status.Revised]:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

        query = f"SELECT COUNT(*) FROM research_papers WHERE status = '{status}';"
        result = await db.execute(query)
        count = result.scalar()
        return count

    @staticmethod
    async def get_number_of_research_proposal_by_approve(db: Session):
        # Get counts for all statuses
        approved_count = await AllInformationService.get_number_of_research_proposal_by_status(db, Status.Approved)
        rejected_count = await AllInformationService.get_number_of_research_proposal_by_status(db, Status.Rejected)
        pending_count = await AllInformationService.get_number_of_research_proposal_by_status(db, Status.Pending)
        revised_count = await AllInformationService.get_number_of_research_proposal_by_status(db, Status.Revised)

        return {
            "Research": "Number of Research based on status",
            "Counts": {
                Status.Approved: approved_count,
                Status.Rejected: rejected_count,
                Status.Pending: pending_count,
                Status.Revised: revised_count
            }
        }
    
    @staticmethod
    async def get_number_ethics(db: Session):
        query = f"SELECT COUNT(*) FROM ethics;"
        result = await db.execute(query)
        count = result.scalar()
        return count
    
    @staticmethod
    async def get_number_manuscript(db: Session):
        query = f"SELECT COUNT(*) FROM full_manuscript;"
        result = await db.execute(query)
        count = result.scalar()
        return count
    
    @staticmethod
    async def get_number_copyright(db: Session):
        query = f"SELECT COUNT(*) FROM copyright;"
        result = await db.execute(query)
        count = result.scalar()
        return count
    
    # @staticmethod
    # async def get_research_status_by_course_section(db: Session, course: str, section: str):
    #     # Get the status of papers based on student course and section
    #     query = (
    #         f"SELECT research_papers.status, COUNT(*) as count "
    #         f"FROM research_papers "
    #         f"JOIN authors ON research_papers.id = authors.research_paper_id "
    #         f"JOIN users ON authors.user_id = users.id "
    #         f"JOIN student ON users.student_id = student.id "
    #         f"WHERE student.course = '{course}' AND student.section = '{section}' "
    #         f"GROUP BY research_papers.status;"
    #     )
    #     result = await db.execute(query)
    #     status_counts = result.all()
    #     return status_counts
    
    
    #FOR RESEARCH ADVISER ================= INFOR ABOUT THE RESEARCH  papers they are under to
    @staticmethod
    async def get_number_of_my_advisory(db: AsyncSession, adviser_id: str):
        # Get the number of research papers with a specific adviser
        query = (
            select(func.count())
            .where(ResearchPaper.research_adviser == adviser_id)
        )

        result = await db.execute(query)
        count = result.scalar()
        return count
    
    @staticmethod
    async def get_number_of_advisory_by_status(db: Session, adviser_id: str, status: str):
        # Get the number of research papers with a specific adviser and status
        query = (
            select(func.count())
            .where((ResearchPaper.research_adviser == adviser_id) & (ResearchPaper.status == status))
        )
        
        result = await db.execute(query)
        count = result.scalar()
        return count
    
    @staticmethod
    async def get_number_of_ethics_by_adviser(db: Session, adviser_id: str):
        # Get the number of Ethics associated with research papers for a specific adviser
        query = (
            select(func.count(Ethics.id))
            .join(ResearchPaper, Ethics.research_paper_id == ResearchPaper.id)
            .where(ResearchPaper.research_adviser == adviser_id)
        )
        
        count = await db.execute(query)
        return count.scalar()
    
    @staticmethod
    async def get_number_of_copyright_by_adviser(db: Session, adviser_id: str):
        # Get the number of Ethics associated with research papers for a specific adviser
        query = (
            select(func.count(CopyRight.id))
            .join(ResearchPaper, CopyRight.research_paper_id == ResearchPaper.id)
            .where(ResearchPaper.research_adviser == adviser_id)
        )
        
        count = await db.execute(query)
        return count.scalar()
    
    @staticmethod
    async def get_number_of_full_manuscript_by_adviser(db: Session, adviser_id: str):
        # Get the number of Ethics associated with research papers for a specific adviser
        query = (
            select(func.count(FullManuscript.id))
            .join(ResearchPaper, FullManuscript.research_paper_id == ResearchPaper.id)
            .where(ResearchPaper.research_adviser == adviser_id)
        )
        
        count = await db.execute(query)
        return count.scalar()
    
    @staticmethod
    async def get_status_count_of_proposal_by_adviser(db: Session, adviser_id: str):
        # Get the number of research papers with a specific adviser and status
        query = (
            select(
                ResearchPaper.status,
                func.count().label("count")
            )
            .where(ResearchPaper.research_adviser == adviser_id)
            .group_by(ResearchPaper.status)
            .having(func.count() > 0)
        )

        result = await db.execute(query)
        status_counts = result.fetchall()
        return status_counts
    
    @staticmethod
    async def get_status_count_of_ethics_by_adviser(db: Session, adviser_id: str):
        # Get the number of Ethics statuses associated with research papers for a specific adviser
        query = (
            select(
                Ethics.status,
                func.count().label("count")
            )
            .join(ResearchPaper, ResearchPaper.id == Ethics.research_paper_id)
            .where(ResearchPaper.research_adviser == adviser_id)
            .group_by(Ethics.status)
            .having(func.count() > 0)
        )

        result = await db.execute(query)
        status_counts = result.fetchall()
        return status_counts
        
    @staticmethod
    async def get_status_count_of_copyright_by_adviser(db: Session, adviser_id: str):
        query = (
            select(
                CopyRight.status,
                func.count().label("count")
            )
            .join(ResearchPaper, ResearchPaper.id == CopyRight.research_paper_id)
            .where(ResearchPaper.research_adviser == adviser_id)
            .group_by(CopyRight.status)
            .having(func.count() > 0)
        )

        result = await db.execute(query)
        status_counts = result.fetchall()
        return status_counts
    
    @staticmethod
    async def get_status_count_of_full_manuscript_by_adviser(db: Session, adviser_id: str):
        query = (
            select(
                FullManuscript.status,
                func.count().label("count")
            )
            .join(ResearchPaper, ResearchPaper.id == FullManuscript.research_paper_id)
            .where(ResearchPaper.research_adviser == adviser_id)
            .group_by(FullManuscript.status)
            .having(func.count() > 0)
        )

        result = await db.execute(query)
        status_counts = result.fetchall()
        return status_counts
    
    
    
    #Mahirap na part kasi yung class information ng user sa db ni jocarl mahirap kunin
    @staticmethod
    async def get_research_status_by_course_section(db: Session, class_id: str):
        query = (
            select(
                FullManuscript.status,
                func.count().label("count")
            )
            .join(ResearchPaper, ResearchPaper.id == FullManuscript.research_paper_id)
            .where(ResearchPaper.research_adviser == adviser_id)
            .group_by(FullManuscript.status)
            .having(func.count() > 0)
        )

        result = await db.execute(query)
        status_counts = result.fetchall()
        return status_counts