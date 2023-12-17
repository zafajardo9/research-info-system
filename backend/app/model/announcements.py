from typing import List, Optional
from app.model.mixins import TimeMixin
from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field, Relationship



class Announcement(SQLModel, TimeMixin, table=True):
    __tablename__ = "announcements"

    id: Optional[str] = Field(primary_key=True, nullable=False)
    user_id: str = Field(nullable=True)
    user_role_target: str
    announcement_type: str
    title: str
    content: str
    other_details: Optional[str]
    

