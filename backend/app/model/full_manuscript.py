
from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship



class FullManuscript(SQLModel, TimeMixin, table=True):
    __tablename__ = "full_manuscript"


    id: Optional[str] = Field(primary_key=True)

    research_paper_id: str = Field(foreign_key="research_papers.id")
    content: str
    keywords: str
    file: str
    abstract: str




    
    status: str


    research_paper: "ResearchPaper" = Relationship(back_populates="full_manuscript")

    