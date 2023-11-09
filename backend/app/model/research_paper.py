# from app.model.users import Users

from typing import List, Optional
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlmodel import SQLModel, Field, Relationship

from app.model.research_status import ResearchPaperStatus

class Author(SQLModel, table=True):
    __tablename__ = "authors"

    id: int = Field(primary_key=True)
    name: str #not needed
    user_id: int = Field(foreign_key="users.id")
    research_paper_id: int = Field(foreign_key="research_papers.id")


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

    # Define a one-to-many relationship to link authors to research papers
    authors: List[Author] = Relationship(back_populates="research_paper")

    # Define a one-to-one relationship to link the research paper status
    status: Optional[ResearchPaperStatus] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="research_paper"
    )



