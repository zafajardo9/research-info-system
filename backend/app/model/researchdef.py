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
