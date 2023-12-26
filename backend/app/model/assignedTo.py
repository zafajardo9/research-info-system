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
    class_id: str = Field(foreign_key="class.id")
    research_type_id: Optional[str] = Field(default=None, foreign_key="research_types_assigned.id")

    research_type: Optional["AssignedResearchType"] = Relationship(back_populates="course_section")
    
    #Relationship
    class_: "Class" = Relationship(back_populates="assigned_sections") 




class AssignedSectionsToProf(SQLModel, table=True):
    __tablename__ = "section_assigned_prof"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    class_id: str = Field(foreign_key="class.id")
    
    user_id: str = Field(default=None, foreign_key="users.id")
    users: List["Users"] = Relationship(back_populates="section_assigned_prof")
    
    
    #Setting up relation
    class_: "Class" = Relationship(back_populates="assign_section_prof") 
    
    


