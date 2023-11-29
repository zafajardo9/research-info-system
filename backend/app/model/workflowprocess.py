from typing import List, Optional
from datetime import date
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
    copyright:  List["Ethics"] = Relationship(back_populates="workflow_step")
    full_manuscript: List["Ethics"] = Relationship(back_populates="workflow_step")
