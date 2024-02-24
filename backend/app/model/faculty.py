from datetime import date
from typing import Optional
from sqlalchemy import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from app.model.mixins import TimeMixin

class Faculty(SQLModel, table=True):
    __tablename__ = "FISFaculty"

    FacultyId: Optional[int] = Field(None, primary_key=True, nullable=False)
    FirstName: str = Column(name="FirstName")
    LastName: str = Column(name="LastName")
    MiddleName: str = Column(name="MiddleName")
    MiddleInitial: str = Column(name="MiddleInitial")
    BirthDate: date = Column(name="BirthDate")
    MobileNumber: str = Column(name="MobileNumber")
    
    
    Email: str = Column(name="Email")
    Password: str = Column(name="Password")

    users: Optional["Users"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="faculty")