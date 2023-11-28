from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship

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

class Process(SQLModel, table=True):
    __tablename__ = "process"

    id: str = Field(primary_key=True)
    course: Course
    year: str
    user_id: str = Field(foreign_key="users.id")


    proposal: bool
    pre_oral_defense: bool
    ethics: bool
    full_manu: bool
    final_defense: bool
    copy: bool
    
