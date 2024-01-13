from collections import defaultdict
from datetime import datetime
from itertools import groupby
import logging
from operator import attrgetter
import uuid
from sqlalchemy import delete, join, and_, update
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select
from typing import List, Optional
import uuid
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException


from app.repository.notif_repo import NotificationRepository


from app.schema import NavigationTabCreate, NavigationProcessDisplay, NavigationTabUpdate

from app.model import Notification, Users, Author, Student, Faculty

from app.model import ResearchPaper, ResearchDefense, FullManuscript, CopyRight, Ethics



class NotificationService:
    
    
    @staticmethod
    async def display_my_notif(user_id: str):
        try:
            # Fetch assigned sections for the user
            first_query = select(Notification).where(Notification.user_id == user_id)
            assigns = await db.execute(first_query)
            assigns = assigns.fetchall()
            assignments_list = [dict(assign) for assign in assigns]
            return assignments_list
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @staticmethod
    async def create_notif(user_id: str, message: str):
        notif_id = str(uuid.uuid4())
        created = Notification(
                    id = notif_id,
                    user_id = user_id,
                    message = message,
                    isRead = False, 
                    )
        db.add(created)
        await db.commit()
        
    # PAG NAG CREATE OPTION 1
    @staticmethod
    async def _user_participated_paper(research_paper_id: str):
        try:
            authors_query = (
                select(
                    Users.id,
                    )
                .join(Author, Users.id == Author.user_id)
                .join(ResearchPaper, ResearchPaper.id == Author.research_paper_id)
                .where(ResearchPaper.id == research_paper_id)
            )
            authors_result = await db.execute(authors_query)
            authors_details = authors_result.fetchall()

            for author_id in authors_details:
                await NotificationService.create_notif(author_id[0], "You are one of the authors for a research paper")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
    
    
    @staticmethod
    async def delete_all_user_notif(user_id: str):
        try:
            stmt = delete(Notification).where(Notification.user_id == user_id)
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            print(f"Error Deleting all: {e}")
            raise
        
    @staticmethod
    async def delete_selected(notif_id: str):
        try:
            stmt = delete(Notification).where(Notification.id == notif_id)
            print(stmt)  # Check the generated SQL statement
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            print(f"Error deleting this: {e}")
            raise