from datetime import datetime
import logging
import uuid
from sqlalchemy import insert, join
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.announcement_repo import AnnouncementRepository
from app.schema import AnnouncementCreate, AnnouncementDisplay, ResponseSchema
from app.model import Users, Faculty, Announcement

class AnnouncementService:
    
    @staticmethod
    async def create_announcement(data: AnnouncementCreate, user_id: str):
        announcement_id = str(uuid.uuid4()) 
        db_assign_research = Announcement(id=announcement_id, user_id = user_id, **data.dict())
        db.add(db_assign_research)
        await db.commit()
        await db.refresh(db_assign_research)
        return db_assign_research


    @staticmethod
    async def get_announcements_with_user_names() -> List[AnnouncementDisplay]:
        query = (
            select(
                Announcement,
                Users,
                Faculty
            )
            .join(Users, Announcement.user_id == Users.id)
            .join(Faculty, Users.faculty_id == Faculty.id)
        )
        result = await db.execute(query)
        announcements = result.scalars().all()

        return [
            AnnouncementDisplay(
                user_name=faculty.name,  # Access the Faculty's name
                user_role_target=announcement.user_role_target,
                title=announcement.title,
                content=announcement.content,
                other_details=announcement.other_details,
                created_at=announcement.created_at,
                modified_at=announcement.modified_at,
            )
            for announcement, user, faculty, *extra in announcements
        ]