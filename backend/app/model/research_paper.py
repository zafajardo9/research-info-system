# from app.model.users import Users

from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship



class Author(SQLModel, table=True):
    __tablename__ = "RISauthors"

    id: Optional[str] = Field(primary_key=True)
    user_id: str = Field(foreign_key="RISUsers.id")
    research_paper_id: str = Field(foreign_key="RISresearch_papers.id")

    # Define the relationship to Users
    user: Optional["Users"] = Relationship(back_populates="author", sa_relationship_kwargs={'uselist': False})
    research_paper: Optional["ResearchPaper"] = Relationship(back_populates="authors")


class Status(str, Enum):
    #Faculty
    Approve = "Approve"
    Reject = "Rejected"
    Pending = "Pending"
    Revise = "Revise" # if magpapa revise si faculty
    Revised = "Revised" #pag ang student nag revise nung pinasa
    
    Approved = "Approved"
    Rejected = "Rejected"
    

class ResearchPaper(SQLModel, TimeMixin, table=True):
    __tablename__ = 'RISresearch_papers'

    id: Optional[str] = Field(primary_key=True)
    title: str

    research_type: str
    submitted_date: date
    status: Status = Status.Pending

    file_path: str
    research_adviser: str
        # EXTENSIOOOOONNNNN
    extension: Optional[str]
    #extension_type: Optional[str]
    
    
    workflow_step_id: str = Field(foreign_key="RISworkflow_steps.id")
    workflow_step: "WorkflowStep" = Relationship(back_populates="research_paper")

    authors: Optional[List["Author"]] = Relationship(back_populates="research_paper")
    comments: Optional[List["Comment"]] = Relationship(back_populates="research_paper")

    ethics: "Ethics" = Relationship(back_populates="research_paper")
    full_manuscript: "FullManuscript" = Relationship(back_populates="research_paper")
    copyright: "CopyRight" = Relationship(back_populates="research_paper")
    research_defense: List["ResearchDefense"] = Relationship(back_populates="research_paper")



class FacultyResearchPaper(SQLModel, TimeMixin, table=True):
    __tablename__ = 'RISfaculty_research_papers'

    id: str = Field(primary_key=True)
    title: str
    content: str
    abstract: str
    file_path: str
    date_publish: Optional[date]
    category: str
    keywords: str
    publisher: str
    status: Optional[str]
    
    user_id: Optional[str] = Field(default=None, foreign_key="RISUsers.id")

    user: Optional["Users"] = Relationship(back_populates="faculty_research_papers")
    
    