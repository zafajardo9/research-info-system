from typing import List, Optional
from datetime import date

from pydantic import BaseModel
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from app.model.research_paper import Status

class Course(str, Enum):
    BSIT = "BSIT"
    BSENTREP = "BSENTREP"
    BTLEDICT = "BTLEDICT"
    BSBAMM = "BSBAMM"
    BBTLEDHE = "BBTLEDHE"
    BSBAHRM = "BSBAHRM"
    BPAPFM = "BPAPFM"
    DOMTMOM = "DOMTMOM"

class WorkflowClass(SQLModel, table=True):
    #HANDLES ONE TO MANY
    __tablename__ = "workflow_class"


    id: str = Field(primary_key=True)

    workflow_id: str = Field(default=None, foreign_key="workflow.id", primary_key=True)
    class_id: str = Field(default=None, foreign_key="class.id", primary_key=True)



class Workflow(SQLModel, table=True):
    __tablename__ = "workflow"

    id: str = Field(primary_key=True)
    type: str
    user_id: str = Field(foreign_key="users.id") #user na nag set nung flow

    steps: List["WorkflowStep"] = Relationship(back_populates="workflow")
    
    
    users: "Users" = Relationship(back_populates="workflow")
    class_: List["Class"] = Relationship(back_populates="workflows", link_model= WorkflowClass)

    
class WorkflowStep(SQLModel, table=True):
    __tablename__ = "workflow_steps"

    id: str = Field(primary_key=True)
    name: str
    description: str
    workflow_id: str = Field(foreign_key="workflow.id")
    workflow: "Workflow" = Relationship(back_populates="steps")
    
    research_paper: List["ResearchPaper"] = Relationship(back_populates="workflow_step")
    ethics: List["Ethics"] = Relationship(back_populates="workflow_step")
    copyright:  List["CopyRight"] = Relationship(back_populates="workflow_step")
    full_manuscript: List["FullManuscript"] = Relationship(back_populates="workflow_step")



# ==========================================

class NavigationTab(SQLModel, table=True):
    __tablename__ = "navigation_role"

    id: str = Field(primary_key=True, index=True, unique=True)
    role: str
    #class_id: str = Field(foreign_key="class.id")
    class_id: str
    type: str
    has_submitted_proposal: bool = Field(default=False)
    has_pre_oral_defense_date: bool = Field(default=False)
    has_submitted_ethics_protocol: bool = Field(default=False)
    has_submitted_full_manuscript: bool = Field(default=False)
    has_set_final_defense_date: bool = Field(default=False)
    has_submitted_copyright: bool = Field(default=False)
    
    #Relationship
    #class_: "Class" = Relationship(back_populates="navigation_tab") 


#if role research adviser assigned research type and section course... dito sa navigation tab checker nung role then section course tapos type
#table na to for research adviser and prof