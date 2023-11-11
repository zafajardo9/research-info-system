# from app.model.users import Users

from typing import List, Optional
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlmodel import SQLModel, Field, Relationship




class Author(SQLModel, table=True):
    __tablename__ = "authors"

    id: int = Field(primary_key=True)
    name: str
    user_id: int = Field(foreign_key="users.id")
    research_paper_id: int = Field(foreign_key="research_papers.id")

    research_paper: Optional["ResearchPaper"] = Relationship(back_populates="authors")

class ResearchPaper(SQLModel, table=True):
    __tablename__ = 'research_papers'

    id: int = Field(primary_key=True)
    title: str
    content: str
    abstract: str
    research_type: str
    submitted_date: datetime
    keywords: str
    file_path: str
    research_adviser: int

    authors: List[Author] = Relationship(back_populates="research_paper")

    # status_id: Optional[int] = Field(foreign_key="research_papers_status.id")
    # status: Optional["ResearchPaperStatus"] = Relationship(back_populates="research_paper")
