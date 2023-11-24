from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship


class CopyRight(SQLModel, TimeMixin, table=True):
    __tablename__ = "copyright"


    id: Optional[str] = Field(primary_key=True)

    research_paper_id: str = Field(foreign_key="research_papers.id")

    co_authorship: Optional[str] = None
    affidavit_co_ownership: Optional[str] = None
    joint_authorship: Optional[str] = None
    approval_sheet: Optional[str] = None
    receipt_payment: Optional[str] = None
    recordal_slip: Optional[str] = None
    acknowledgement_receipt: Optional[str] = None
    certificate_copyright: Optional[str] = None
    recordal_template: Optional[str] = None
    ureb_18: Optional[str] = None
    journal_publication: Optional[str] = None


    copyright_manuscript: Optional[str] = None


    research_paper: "ResearchPaper" = Relationship(back_populates="copyright")