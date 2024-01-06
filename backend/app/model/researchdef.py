from typing import List, Optional
from app.model.mixins import TimeMixin
from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field, Relationship

from datetime import date



class ResearchDefense(SQLModel, TimeMixin, table=True):
    __tablename__ = "research_defense"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    research_paper_id: str = Field(foreign_key="research_papers.id")
    type: str
    date: date
    
    workflow_step_id: str = Field(foreign_key="workflow_steps.id")
    
    
    
    workflow_step: "WorkflowStep" = Relationship(back_populates="research_defense")
    research_paper: "ResearchPaper" = Relationship(back_populates="research_defense")
