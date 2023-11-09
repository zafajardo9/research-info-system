from typing import List, Optional
from app.model.mixins import TimeMixin
from app.model.faculty import Faculty
from app.model.research_paper import Author, ResearchPaper
from app.model.student import Student
from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field, Relationship





# class Users(SQLModel, TimeMixin, table=True):
#     __tablename__ = "users"

#     id: Optional[int] = Field(primary_key=True, nullable=False)
#     username: str = Field(sa_column=Column("username", String, unique=True))
#     email: str = Field(sa_column=Column("email", String, unique=True))
#     password: str


#     student_number: Optional[str] = Field(sa_column=Column("student_number", String), nullable=True)
    
#     student_id: Optional[int] = Field(default=None, foreign_key="student.id")
#     faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")

#     student: Optional["Student"] = Relationship(back_populates="users")
#     faculty: Optional["Faculty"] = Relationship(back_populates="users")

#     roles: str
    
    
#     # Define relationships to access related data
#     research_papers = Relationship(back_populates="adviser")
#     authors = Relationship(back_populates="user")


class Users(SQLModel, TimeMixin, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(primary_key=True, nullable=False)
    username: str = Field(sa_column=Column("username", String, unique=True))
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str

    student_number: Optional[str] = Field(sa_column=Column("student_number", String))
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")

    student: Optional["Student"] = Relationship(back_populates="users")
    faculty: Optional["Faculty"] = Relationship(back_populates="users")

    roles: str

    # # Define relationships to access related data
    # research_papers: Optional["ResearchPaper"] = Relationship(back_populates="research_adviser")
    # authors: Optional["Author"] = Relationship(back_populates="user")



