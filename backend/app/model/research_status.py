from typing import List, Optional
from app.model.mixins import TimeMixin

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlmodel import SQLModel, Field, Relationship

class ResearchPaperStatus(SQLModel, TimeMixin, table=True):
    __tablename__ = 'research_papers_status'

    id: int = Field(primary_key=True)
    proposal: bool
    under_review: bool
    research_protocol: bool
    abstract: str

    accepted: bool
    published: bool

    research_adviser: int

class Comment(SQLModel, TimeMixin, table=True):
    __tablename__ = 'comments'

    id: int = Field(primary_key=True)
    text: str
    research_paper_status_id: int = Field(foreign_key="research_papers_status.id")
    
    research_paper_status: ResearchPaperStatus = relationship("ResearchPaperStatus", back_populates="comments")

