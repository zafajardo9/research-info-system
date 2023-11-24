# from app.model.users import Users

from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship



class Author(SQLModel, table=True):
    __tablename__ = "authors"

    id: Optional[str] = Field(primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    research_paper_id: str = Field(foreign_key="research_papers.id")

    # Define the relationship to Users
    user: Optional["Users"] = Relationship(back_populates="author", sa_relationship_kwargs={'uselist': False})
    research_paper: Optional["ResearchPaper"] = Relationship(back_populates="authors")


class Status(str, Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"
    Revised = "Revised"

class ResearchPaper(SQLModel, TimeMixin, table=True):
    __tablename__ = 'research_papers'

    id: Optional[str] = Field(primary_key=True)
    title: str

    research_type: str
    submitted_date: date
    status: Status = Status.Pending

    file_path: str
    research_adviser: str

    authors: Optional[List["Author"]] = Relationship(back_populates="research_paper")
    comments: Optional[List["Comment"]] = Relationship(back_populates="research_paper")

    ethics: Optional["Ethics"] = Relationship(back_populates="research_paper")
    full_manuscript: Optional["FullManuscript"] = Relationship(back_populates="research_paper")
    copyright: Optional["CopyRight"] = Relationship(back_populates="research_paper")

