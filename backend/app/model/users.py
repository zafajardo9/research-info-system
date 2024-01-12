from typing import List, Optional
from app.model.mixins import TimeMixin
from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field, Relationship

class UsersRole(SQLModel, TimeMixin,table=True):
    __tablename__= "RISuser_role"

    users_id: Optional[str] = Field(default=None, foreign_key="RISUsers.id",primary_key=True)
    role_id: Optional[str] = Field(default=None, foreign_key="RISrole.id",primary_key=True)


class Role(SQLModel, TimeMixin, table=True):
    __tablename__ = "RISrole"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    role_name: str

    users: List["Users"] = Relationship(back_populates="roles", link_model=UsersRole)

class Users(SQLModel, TimeMixin, table=True):
    __tablename__ = "RISUsers"

    id: Optional[str] = Field(primary_key=True, nullable=False)

    student_id: Optional[int] = Field(default=None, foreign_key="SPSStudent.StudentId") 
    faculty_id: Optional[int] = Field(default=None, foreign_key="FISFaculty.FacultyId")


    # PANG CONNECT=================

    student: Optional["Student"] = Relationship(back_populates="users")
    faculty: Optional["Faculty"] = Relationship(back_populates="users")
    
    roles: List["Role"] = Relationship(back_populates="users", link_model=UsersRole)

    
    author: Optional[List["Author"]] = Relationship(back_populates="user")
    comments: Optional[List["Comment"]] = Relationship(back_populates="user")

      
    workflow: List["Workflow"] = Relationship(back_populates="users")
    
    notifications: Optional[List["Notification"]] = Relationship(back_populates="user")
    
    
    #reltionship to faculty research papers:
    faculty_research_papers: List["FacultyResearchPaper"] = Relationship(back_populates="user")
    
    #iba to ewan
    research_types: Optional[List["AssignedResearchType"]] = Relationship(back_populates="users")
   
    # research_type_assigned_prof: Optional[List["AssignedResearchTypeToProf"]] = Relationship(back_populates="users")
    section_assigned_prof: Optional[List["AssignedSectionsToProf"]] = Relationship(back_populates="users")






