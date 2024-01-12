
from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship

from app.model.research_paper import Status



class Ethics(SQLModel, TimeMixin, table=True):
    __tablename__ = "RISethics"


    id: Optional[str] = Field(primary_key=True)

    research_paper_id: str = Field(foreign_key="RISresearch_papers.id")

    letter_of_intent: Optional[str] = Field(default=None)
    urec_9: Optional[str] = Field(default=None)
    urec_10: Optional[str] = Field(default=None)
    urec_11: Optional[str] = Field(default=None)
    urec_12: Optional[str] = Field(default=None)
    certificate_of_validation: Optional[str] = Field(default=None)
    co_authorship: Optional[str] = Field(default=None)
    status: Status = Status.Pending

    workflow_step_id: str = Field(foreign_key="RISworkflow_steps.id")
    workflow_step: "WorkflowStep" = Relationship(back_populates="ethics")

    research_paper: "ResearchPaper" = Relationship(back_populates="ethics")

    