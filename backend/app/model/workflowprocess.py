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




class Workflow(SQLModel, table=True):
    __tablename__ = "workflow"

    id: str = Field(primary_key=True)
    course: Course
    year: str
    type: str
    user_id: str = Field(foreign_key="users.id") #user na nag set nung flow

    steps: List["WorkflowStep"] = Relationship(back_populates="workflow")
    users: "Users" = Relationship(back_populates="workflow")

    
class WorkflowStep(SQLModel, table=True):
    __tablename__ = "workflow_steps"

    id: str = Field(primary_key=True)
    name: str
    description: str
    step_number: str
    workflow_id: str = Field(foreign_key="workflow.id")
    workflow: "Workflow" = Relationship(back_populates="steps")
    
    research_paper: List["ResearchPaper"] = Relationship(back_populates="workflow_step")
    ethics: List["Ethics"] = Relationship(back_populates="workflow_step")
    copyright:  List["CopyRight"] = Relationship(back_populates="workflow_step")
    full_manuscript: List["FullManuscript"] = Relationship(back_populates="workflow_step")


# todo LIST
# Submitted Proposal
# Pre-Oral Defense Date
# Submitted Ethics/Protocol
# Submitted Full Manuscript
# Set Final Defense Date
# Submitted Copyright

class NavigationTab(SQLModel, table=True):
    __tablename__ = "navigation_role"

    id: str = Field(primary_key=True, index=True, unique=True)
    role: str
    section: str
    course: str
    type: str
    has_submitted_proposal: bool = Field(default=False)
    has_pre_oral_defense_date: bool = Field(default=False)
    has_submitted_ethics_protocol: bool = Field(default=False)
    has_submitted_full_manuscript: bool = Field(default=False)
    has_set_final_defense_date: bool = Field(default=False)
    has_submitted_copyright: bool = Field(default=False)


#if role research adviser assigned research type and section course... dito sa navigation tab checker nung role then section course tapos type
#table na to for research adviser and prof