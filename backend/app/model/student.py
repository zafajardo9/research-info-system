from datetime import date
from typing import Optional
from sqlalchemy import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin

class Student(SQLModel, TimeMixin, table=True):
    __tablename__ = "student"

    id: Optional[int] = Field(primary_key=True, nullable=False)
    name: str
    birth: date
    year: int
    section: str
    course: str
    student_number: str
    phone_number: str

    users: Optional["Users"] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates="student")
