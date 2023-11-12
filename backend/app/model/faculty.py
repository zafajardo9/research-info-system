from datetime import date
from typing import Optional
from sqlalchemy import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin

class Faculty(SQLModel, TimeMixin, table=True):
    __tablename__ = "faculty"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    name: str
    birth: date
    phone_number: str

    users: Optional["Users"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="faculty")