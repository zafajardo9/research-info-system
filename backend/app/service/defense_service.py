from datetime import datetime
import logging
import uuid
from sqlalchemy import insert, join
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy import and_
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
from app.schema import DefenseCreate, DefenseUpdate
from app.model import ResearchDefense

class DefenseService:
    
        
    @staticmethod
    async def create_defense(data: DefenseCreate):
        
        gen_id = str(uuid.uuid4())
        # Parse the date and time strings into date and time objects
        defense_date = datetime.strptime(data.date, "%Y-%m-%d").date()
        defense_time = datetime.strptime(data.time, "%H:%M:%S").time()
        # Create the ResearchDefense instance with the parsed date and time
        db_make = ResearchDefense(
            id=gen_id, 
            type=data.type, 
            date=defense_date, 
            time=defense_time, 
            research_paper_id=data.research_paper_id,
            workflow_step_id = data.workflow_step_id
            )
        db.add(db_make)
        await db.commit()
        await db.refresh(db_make)
        return db_make
    
    
    @staticmethod
    async def display_by_research_step(research_paper_id: str, workflowstep_id: str):
        query = (
            select(ResearchDefense)
            .where(and_(
                ResearchDefense.research_paper_id == research_paper_id,
                ResearchDefense.workflow_step_id == workflowstep_id
            ))
        )
        result = await db.execute(query)
        defense = result.scalar()
        
        return defense
    
    @staticmethod
    async def display_by_id(defense_id: str):
        query = (
            select(ResearchDefense)
            .where(ResearchDefense.id == defense_id)
        )
        result = await db.execute(query)
        defense = result.scalar()
        
        return defense
    
    @staticmethod
    async def update_defense(defense_id: str, data: DefenseUpdate):
        query = select(ResearchDefense).filter_by(id=defense_id)
        
        query_defense = await db.execute(query)
        defense = query_defense.scalar()
        
        if not defense:
            raise HTTPException(status_code=404, detail="Defense not found")

        update_data = data.dict(exclude_unset=True)
        
        if 'date' in update_data:
            update_data['date'] = datetime.strptime(update_data['date'], "%Y-%m-%d").date()
        if 'time' in update_data:
            update_data['time'] = datetime.strptime(update_data['time'], "%H:%M:%S").time()
    
        for key, value in update_data.items():
            setattr(defense, key, value)
        await db.commit()
        await db.refresh(defense)
        
        return defense
    
    
    @staticmethod
    async def delete_def(defense_id: str):
        print(f"Deleting announcement with ID: {defense_id}")

        query = delete(ResearchDefense).where(ResearchDefense.id == defense_id)
        
        result = await db.execute(query)
        await db.commit()
        if result.rowcount > 0:
            return True 
        else:
            return False

