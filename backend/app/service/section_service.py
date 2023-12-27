from datetime import datetime
import logging
import uuid
from sqlalchemy import and_, insert, join
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

from app.schema import ClassCreate, FullManuscriptResponse
from app.model import Users, Class, Student

class SectionService:
        
    # @staticmethod
    # async def input_section_course(class_create: ClassCreate):
    #     id = str(uuid.uuid4())  # Generate UUID for workflow_id
    #     db_class = Class(id=id, **class_create.dict())
    #     db.add(db_class)
    #     await db.commit()
    #     await db.refresh(db_class)
    #     return db_class
    
    
    @staticmethod
    async def find_section_course(section: str, course:str):
        query = select(Class).where(Class.section == section).where(Class.course == course)
        return (await db.execute(query)).scalar_one_or_none()
    
    @staticmethod
    async def what_section_course(class_id: str):
        query = select(Class).where(Class.id == class_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def check_and_input_section_course(class_create: ClassCreate):
        # Check if the section and course already exist
        query = select(Class).where(Class.course == class_create.course).where(Class.section == class_create.section)
        existing_sections = await db.execute(query)
        records = existing_sections.all()

        # If the section and course do not exist, create a new record
        if not records:
            id = str(uuid.uuid4())  # Generate UUID for section_id
            db_section = Class(id=id, **class_create.dict())
            db.add(db_section)
            await db.commit()
            await db.refresh(db_section)
            return db_section
        else:
            return None
    
    @staticmethod
    async def display_all_sections():
        try:
            # Fetch assigned sections for the user
            first_query = select(Class)
            get_all = await db.execute(first_query)
            all = get_all.fetchall()

            if not all:
                return None  # Return None when no assignments are found

            return all

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        
    @staticmethod
    async def delete_section(id: str):
            # Delete workflow steps
        await db.execute(delete(Class).where(Class.id == id))

        return True
    
    @staticmethod
    async def delete_all_section():
            # Delete workflow steps
        await db.execute(delete(Class))

        return True