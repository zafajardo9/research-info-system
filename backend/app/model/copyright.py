from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship

from app.model.research_paper import Status


class CopyRight(SQLModel, TimeMixin, table=True):
    __tablename__ = "copyright"


    id: Optional[str] = Field(primary_key=True)

    research_paper_id: str = Field(foreign_key="research_papers.id")

    co_authorship: Optional[str] = Field(default=None)
    affidavit_co_ownership: Optional[str] = Field(default=None)
    joint_authorship: Optional[str] = Field(default=None)
    approval_sheet: Optional[str] = Field(default=None)
    receipt_payment: Optional[str] = Field(default=None)
    recordal_slip: Optional[str] = Field(default=None)
    acknowledgement_receipt: Optional[str] = Field(default=None)
    certificate_copyright: Optional[str] = Field(default=None)
    recordal_template: Optional[str] = Field(default=None)
    ureb_18: Optional[str] = Field(default=None)
    journal_publication: Optional[str] = Field(default=None)


    copyright_manuscript: Optional[str] = Field(default=None)
    status: Status = Status.Pending
    workflow_step_id: str = Field(foreign_key="workflow_steps.id")
    workflow_step: "WorkflowStep" = Relationship(back_populates="copyright")

    research_paper: "ResearchPaper" = Relationship(back_populates="copyright")