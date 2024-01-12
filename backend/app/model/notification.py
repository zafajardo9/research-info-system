from typing import List, Optional
from datetime import date
from app.model.mixins import TimeMixin
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlmodel import SQLModel, Field, Relationship


class Notification(SQLModel, TimeMixin, table=True):
    __tablename__ = "RISnotifications"

    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="RISUsers.id") 
    message: str
    isRead: bool

    user: Optional["Users"] = Relationship(back_populates="notifications")
