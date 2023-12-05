from uuid import uuid4
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.model.research_paper import Author
from app.config import db
from app.schema import AuthorSchema
from app.model.announcements import Announcement
from app.repository.base_repo import BaseRepo

class AnnouncementRepository(BaseRepo):
    model = Announcement