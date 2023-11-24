from datetime import datetime
from sqlalchemy import join
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


from app.schema import CopyRightCreate, CopyRightUpdate, CopyRightResponse, ResponseSchema
from app.model import CopyRight
from app.repository.copyright_repo import CopyrightRepository
from app.model.research_paper import Author, ResearchPaper

class CopyrightService:

    @staticmethod
    async def upload_copyright(db: Session, copyright_data: CopyRightCreate):
        _copyright_id = str(uuid4())
        _copyright_paper = CopyRight(
            id = _copyright_id,
            research_paper_id = copyright_data.research_paper_id,
            co_authorship = copyright_data.co_authorship,
            affidavit_co_ownership = copyright_data.affidavit_co_ownership,
            joint_authorship = copyright_data.joint_authorship,
            approval_sheet = copyright_data.approval_sheet,
            receipt_payment = copyright_data.receipt_payment,
            recordal_slip = copyright_data.recordal_slip,
            acknowledgement_receipt = copyright_data.acknowledgement_receipt,
            certificate_copyright = copyright_data.certificate_copyright,
            recordal_template = copyright_data.recordal_template,
            ureb_18 = copyright_data.ureb_18,
            journal_publication = copyright_data.journal_publication,
            copyright_manuscript = copyright_data.copyright_manuscript,
        )

        await CopyrightRepository.create(db, **_copyright_paper.dict())

    @staticmethod
    async def get_copyright_by_research_paper_id(
        db: Session,
        research_paper_id: str
    ) -> Optional[CopyRight]:
        research_paper = await CopyrightRepository.get_by_research_paper_id(db, research_paper_id)
        
        if research_paper is None:
            raise HTTPException(status_code=404, detail="Full Manuscript not found")
        
        return research_paper
    

    @staticmethod
    async def update_copyright(db: AsyncSession, copyright_data: CopyRightUpdate, manuscript_id: str) -> CopyRightResponse:
        try:
            await CopyrightRepository.update_copyright(db, manuscript_id, **copyright_data.dict())
            # Fetch the updated data from the database
            updated_copyright = await CopyrightRepository.get_copyright_by_id(db, manuscript_id)
            return CopyRightResponse(**updated_copyright.dict())
        except HTTPException:
            raise  # Re-raise the HTTPException
        except Exception as e:
            print(f"Error during update: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    @staticmethod
    async def delete_copyright(db: Session, ethics_id: str):
        try:
            # Call the repository method to delete ethics data by ethics ID
            result = await CopyrightRepository.delete_copyright_id(db, ethics_id)

            if not result:
                raise HTTPException(status_code=404, detail="Copyright data not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    @staticmethod
    async def get_manuscript_by_user(db: Session, user_id: str) -> List[CopyRight]:
        query = (
            select(CopyRight)
            .join(ResearchPaper, CopyRight.research_paper_id == ResearchPaper.id)
            .join(Author, ResearchPaper.id == Author.research_paper_id)
            .where(Author.user_id == user_id)
        )
        result = await db.execute(query)
        copyright_list = result.scalars().all()

        if not copyright_list:
            raise HTTPException(status_code=404, detail="Copyright data not found for the user")

        return copyright_list