
from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship



class Ethics(SQLModel, TimeMixin, table=True):
    __tablename__ = "ethics"


    id: Optional[str] = Field(primary_key=True)

    research_paper_id: str = Field(foreign_key="research_papers.id")

    letter_of_intent: str
    urec_9: str
    urec_10: str
    urec_11: str
    urec_12: str
    certificate_of_validation: str
    co_authorship: str


    research_paper: "ResearchPaper" = Relationship(back_populates="ethics")

    