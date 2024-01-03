from datetime import date
from typing import List, Optional
from sqlalchemy import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin
from app.model.workflowprocess import WorkflowClass


    
class Class(SQLModel, table=True):
    __tablename__ = "class"

    id: str = Field(primary_key=True, nullable=False)
    section: str
    course: str
    
    # Add a relationship back to Students through the association table
    students: List["Student"] = Relationship(back_populates="classes")
    
    #navigation_tab: List["NavigationTab"] = Relationship(back_populates="class_")
    
    assigned_sections: List["AssignedSections"] = Relationship(back_populates="class_")
    
    assign_section_prof: List["AssignedSectionsToProf"] = Relationship(back_populates="class_")
    
    #connection to the workflow table
    workflows: List["Workflow"] = Relationship(back_populates="class_", link_model=WorkflowClass)
        
class Student(SQLModel, TimeMixin, table=True):
    __tablename__ = "student"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    name: str
    birth: date
    year: int
    student_number: str
    phone_number: str

    users: Optional["Users"] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates="student")
    
    #referencing to the Class table
    class_id: Optional[str] = Field(foreign_key="class.id")
    classes: List["Class"] = Relationship(back_populates="students")