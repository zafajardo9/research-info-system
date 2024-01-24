from datetime import date
from typing import List, Optional
from sqlalchemy import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from app.model.mixins import TimeMixin
from app.model.workflowprocess import NavigationClass, WorkflowClass


    
class Class(SQLModel, table=True):
    __tablename__ = "RISClass"

    id: str = Field(primary_key=True, nullable=False)
    section: str
    course: str

    assigned_sections: List["AssignedSections"] = Relationship(back_populates="class_")
    
    assign_section_prof: List["AssignedSectionsToProf"] = Relationship(back_populates="class_")
    
    #connection to the workflow table
    workflows: List["Workflow"] = Relationship(back_populates="class_", link_model=WorkflowClass)
    navigation_role: List["NavigationTab"] = Relationship(back_populates="class_id", link_model=NavigationClass)
    set_defense_class: List["SetDefense"] = Relationship(back_populates="class_")
        
class Student(SQLModel, table=True):
    __tablename__ = "SPSStudent"

    StudentId: Optional[int] = Field(primary_key=True, nullable=False)
    FirstName: str
    LastName: str
    MiddleName: str
    DateOfBirth: date
    StudentNumber: str
    MobileNumber: str
    Email: str
    Password: str
    
    
    users: Optional["Users"] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates="student")
    
    #classes: List["Class"] = Relationship(back_populates="students")