from typing import List, Optional
from app.model.mixins import TimeMixin

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship




class Comment(SQLModel, TimeMixin, table=True):
    __tablename__ = 'comments'

    id: Optional[str] = Field(primary_key=True)
    text: str


    name: str
    user_id: str = Field(foreign_key="users.id")
    research_paper_id: str = Field(foreign_key="research_papers.id") 

    user: Optional["Users"] = Relationship(back_populates="comments")
    research_paper: Optional["ResearchPaper"] = Relationship(back_populates="comments")