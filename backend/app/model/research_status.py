from typing import List, Optional
from app.model.mixins import TimeMixin

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship




class Comment(SQLModel, TimeMixin, table=True):
    __tablename__ = 'RIScomments'

    id: Optional[str] = Field(primary_key=True)
    text: str

    user_id: str = Field(foreign_key="RISUsers.id")
    research_paper_id: str = Field(foreign_key="RISresearch_papers.id") 

    user: Optional["Users"] = Relationship(back_populates="comments")
    research_paper: Optional["ResearchPaper"] = Relationship(back_populates="comments")