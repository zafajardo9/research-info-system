from datetime import datetime
import logging
import uuid
from sqlalchemy import insert, join
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select
from typing import Any, Dict, List, Optional
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import commit_rollback, db

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
    async def get_announcements_with_user_names():
        
        query = (
            select(
                Announcement,
                Users.email,
                Faculty.name,
            )
            .join(Users, Announcement.user_id == Users.id)
            .join(Faculty, Users.faculty_id == Faculty.id)
        )
        result = await db.execute(query)
        announcements = result.fetchall()

        return [
            {
                "announcement": {
                    "id": announcement.id,
                    "created_at": announcement.created_at,
                    "announcement_type": announcement.announcement_type,
                    "title": announcement.title,
                    "other_details": announcement.other_details,
                    "modified_at": announcement.modified_at,
                    "user_role_target": announcement.user_role_target,
                    "content": announcement.content
                },
                "user_email": user,
                "faculty_name": faculty
            }
            for announcement, user, faculty, *extra in announcements
        ]
        
        
    @staticmethod
    async def delete_announcement_by_id(announcement_id: str):
        print(f"Deleting announcement with ID: {announcement_id}")

        query = delete(Announcement).where(Announcement.id == announcement_id)
        
        
        result = await db.execute(query)
        
        if result.rowcount > 0:
            return True 
        else:
            return False
        
    @staticmethod
    async def delete_all_announcements_function():
        try:
            delete_statement = delete(Announcement)
            await db.execute(delete_statement)


            return delete_statement
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
            
            
    @staticmethod
    async def get_announcements_students_funding():
        
        query = (
            select(
                Announcement,
                Users.email,
                Faculty.name,
            )
            .join(Users, Announcement.user_id == Users.id)
            .join(Faculty, Users.faculty_id == Faculty.id)
            .where((Announcement.user_role_target == "student") & (Announcement.announcement_type == "funding opportunity"))
        )
        result = await db.execute(query)
        announcements = result.fetchall()

        return [
            {
                "announcement": {
                    "id": announcement.id,
                    "created_at": announcement.created_at,
                    "announcement_type": announcement.announcement_type,
                    "title": announcement.title,
                    "other_details": announcement.other_details,
                    "modified_at": announcement.modified_at,
                    "user_role_target": announcement.user_role_target,
                    "content": announcement.content
                },
                "user_email": user,
                "faculty_name": faculty
            }
            for announcement, user, faculty, *extra in announcements
        ]
        
        

    @staticmethod
    async def get_announcements_students_training():
        
        query = (
            select(
                Announcement,
                Users.email,
                Faculty.name,
            )
            .join(Users, Announcement.user_id == Users.id)
            .join(Faculty, Users.faculty_id == Faculty.id)
            .where((Announcement.user_role_target == "student") & (Announcement.announcement_type == "training and workshop"))
        )
        result = await db.execute(query)
        announcements = result.fetchall()

        return [
            {
                "announcement": {
                    "id": announcement.id,
                    "created_at": announcement.created_at,
                    "announcement_type": announcement.announcement_type,
                    "title": announcement.title,
                    "other_details": announcement.other_details,
                    "modified_at": announcement.modified_at,
                    "user_role_target": announcement.user_role_target,
                    "content": announcement.content
                },
                "user_email": user,
                "faculty_name": faculty
            }
            for announcement, user, faculty, *extra in announcements
        ]
        
        
        
        
    @staticmethod
    async def get_announcements_faculty_funding():
        
        query = (
            select(
                Announcement,
                Users.email,
                Faculty.name,
            )
            .join(Users, Announcement.user_id == Users.id)
            .join(Faculty, Users.faculty_id == Faculty.id)
            .where((Announcement.user_role_target == "faculty") & (Announcement.announcement_type == "funding opportunity"))
        )
        result = await db.execute(query)
        announcements = result.fetchall()

        return [
            {
                "announcement": {
                    "id": announcement.id,
                    "created_at": announcement.created_at,
                    "announcement_type": announcement.announcement_type,
                    "title": announcement.title,
                    "other_details": announcement.other_details,
                    "modified_at": announcement.modified_at,
                    "user_role_target": announcement.user_role_target,
                    "content": announcement.content
                },
                "user_email": user,
                "faculty_name": faculty
            }
            for announcement, user, faculty, *extra in announcements
        ]
        
        

    @staticmethod
    async def get_announcements_faculty_training():
        
        query = (
            select(
                Announcement,
                Users.email,
                Faculty.name,
            )
            .join(Users, Announcement.user_id == Users.id)
            .join(Faculty, Users.faculty_id == Faculty.id)
            .where((Announcement.user_role_target == "faculty") & (Announcement.announcement_type == "training and workshop"))
        )
        result = await db.execute(query)
        announcements = result.fetchall()

        return [
            {
                "announcement": {
                    "id": announcement.id,
                    "created_at": announcement.created_at,
                    "announcement_type": announcement.announcement_type,
                    "title": announcement.title,
                    "other_details": announcement.other_details,
                    "modified_at": announcement.modified_at,
                    "user_role_target": announcement.user_role_target,
                    "content": announcement.content
                },
                "user_email": user,
                "faculty_name": faculty
            }
            for announcement, user, faculty, *extra in announcements
        ]
        
        