from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.author_repo import AuthorRepository
from app.schema import AuthorSchema
from app.model import Users, Author
from app.model.research_paper import Status

class AllInformationService:

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