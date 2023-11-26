
from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship

from app.model.research_paper import Status



class FullManuscript(SQLModel, TimeMixin, table=True):
    __tablename__ = "full_manuscript"


    id: str = Field(primary_key=True)

    research_paper_id: str = Field(foreign_key="research_papers.id")
    content: str = Field(nullable=False)
    keywords: str = Field(nullable=False)
    file: str = Field(nullable=False)
    abstract: str = Field(nullable=False)
    status: Status = Status.Pending
    #para di pwedeng walang laman

    research_paper: "ResearchPaper" = Relationship(back_populates="full_manuscript")

    