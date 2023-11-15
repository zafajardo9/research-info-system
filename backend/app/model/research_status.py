from typing import List, Optional
from app.model.mixins import TimeMixin

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlmodel import SQLModel, Field, Relationship



class ResearchPaperStatus(SQLModel, TimeMixin, table=True):
    __tablename__ = 'research_papers_status'

    id: Optional[str] = Field(primary_key=True)
    research_paper_id: Optional[str] = Field(foreign_key="research_papers.id")
    research_paper: Optional["ResearchPaper"] = Relationship(back_populates="status")

    proposal: bool
    under_review: bool
    research_protocol: bool
    abstract: str

    accepted: bool
    published: bool

    research_adviser: int



class Comment(SQLModel, TimeMixin, table=True):
    __tablename__ = 'comments'

    id: Optional[str] = Field(primary_key=True)
    text: str

    user_id: str = Field(foreign_key="users.id")
    research_paper_id: str = Field(foreign_key="research_papers.id") 

    user: Optional["Users"] = Relationship(back_populates="comments")
    research_paper: Optional["ResearchPaper"] = Relationship(back_populates="comments")