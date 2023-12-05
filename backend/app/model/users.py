from typing import List, Optional
from app.model.mixins import TimeMixin
from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field, Relationship

class UsersRole(SQLModel, TimeMixin,table=True):
    __tablename__= "user_role"

    users_id: Optional[str] = Field(default=None, foreign_key="users.id",primary_key=True)
    role_id: Optional[str] = Field(default=None, foreign_key="role.id",primary_key=True)


class Role(SQLModel, TimeMixin, table=True):
    __tablename__ = "role"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    role_name: str

    users: List["Users"] = Relationship(back_populates="roles", link_model=UsersRole)

class Users(SQLModel, TimeMixin, table=True):
    __tablename__ = "users"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    username: str = Field(sa_column=Column("username", String, unique=True))
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str

    student_number: Optional[str] = Field(sa_column=Column("student_number", String))
    student_id: Optional[str] = Field(default=None, foreign_key="student.id")  # Change the type to String
    faculty_id: Optional[str] = Field(default=None, foreign_key="faculty.id")

    student: Optional["Student"] = Relationship(back_populates="users")
    faculty: Optional["Faculty"] = Relationship(back_populates="users")

    roles: List["Role"] = Relationship(back_populates="users", link_model=UsersRole)

        # Define the relationship to Author and Comment
    author: Optional[List["Author"]] = Relationship(back_populates="user")
    comments: Optional[List["Comment"]] = Relationship(back_populates="user")

        #Setting relation to workflow na magagawa ng user
    workflow: List["Workflow"] = Relationship(back_populates="users")
    
    notifications: Optional[List["Notification"]] = Relationship(back_populates="user")
    

    research_types: Optional[List["AssignedResearchType"]] = Relationship(back_populates="users")
   
    sections_prof: Optional[List["AssignedSectionsToProf"]] = Relationship(back_populates="users")



