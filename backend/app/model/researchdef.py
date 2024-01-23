from typing import List, Optional
from app.model.mixins import TimeMixin
from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field, Relationship

from datetime import date, time



class ResearchDefense(SQLModel, TimeMixin, table=True):
    __tablename__ = "RISresearch_defense"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    research_paper_id: str = Field(foreign_key="RISresearch_papers.id")
    type: str
    date: date
    time: time
    
    workflow_step_id: str = Field(foreign_key="RISworkflow_steps.id")
    
    workflow_step: "WorkflowStep" = Relationship(back_populates="research_defense")
    research_paper: "ResearchPaper" = Relationship(back_populates="research_defense")


class SetDefense(SQLModel, TimeMixin, table=True):
    __tablename__ = "RISset_defense"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    research_type: str
    defense_type: str
    date: date
    time: time
    set_defense_class_handle: List["SetDefenseClass"] = Relationship(back_populates="set_defense")
    

class SetDefenseClass(SQLModel, table=True):
    __tablename__ = "RISset_defense_class"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    class_id: str = Field(foreign_key="RISClass.id")
    set_defense_id: Optional[str] = Field(default=None, foreign_key="RISset_defense.id")

    set_defense: Optional["SetDefense"] = Relationship(back_populates="set_defense_class_handle")
    
    class_: "Class" = Relationship(back_populates="set_defense_class") 