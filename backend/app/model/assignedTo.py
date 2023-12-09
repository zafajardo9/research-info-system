from typing import List, Optional
from app.model.mixins import TimeMixin
from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field, Relationship



class AssignedResearchType(SQLModel, table=True):
    __tablename__ = "research_types_assigned"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    user_id: str = Field(default=None, foreign_key="users.id")
    research_type_name: str

    users: List["Users"] = Relationship(back_populates="research_types")
    course_section: List["AssignedSections"] = Relationship(back_populates="research_type")

    
class AssignedSections(SQLModel, table=True):
    __tablename__ = "sections_course_assigned"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    section: str
    course: str
    research_type_id: Optional[str] = Field(default=None, foreign_key="research_types_assigned.id")

    research_type: Optional["AssignedResearchType"] = Relationship(back_populates="course_section")


class AssignedResearchTypeToProf(SQLModel, table=True):
    __tablename__ = "research_type_assigned_prof"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    user_id: str = Field(default=None, foreign_key="users.id")
    research_type_name: str
    
    users: List["Users"] = Relationship(back_populates="research_type_assigned_prof")
    course_section: List["AssignedSectionsToProf"] = Relationship(back_populates="research_type")

    
class AssignedSectionsToProf(SQLModel, table=True):
    __tablename__ = "section_assigned_prof"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    section: str
    course: str
    research_type_prof_id: Optional[str] = Field(default=None, foreign_key="research_type_assigned_prof.id")

    
    research_type: Optional["AssignedResearchType"] = Relationship(back_populates="course_section")


