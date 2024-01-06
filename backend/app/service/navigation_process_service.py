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


from app.repository.navigation_role_repo import NavigationTabRepository
from app.repository.navigation_class_repo import NavigationClassRepository

from app.model import NavigationClass, NavigationTab
from app.schema import NavigationTabCreate, NavigationProcessDisplay, NavigationTabUpdate
from app.service.section_service import SectionService
from app.model.student import Class


class NavigationProcessService:
    
    
    @staticmethod
    async def create_process_role(navigation_tab: NavigationTabCreate):
        process_id = str(uuid.uuid4())
        db_process = NavigationTab(
            id=process_id,
            role=navigation_tab.role,
            type=navigation_tab.type,
            has_submitted_proposal=navigation_tab.has_submitted_proposal,
            has_pre_oral_defense_date=navigation_tab.has_pre_oral_defense_date,
            has_submitted_ethics_protocol=navigation_tab.has_submitted_ethics_protocol,
            has_submitted_full_manuscript=navigation_tab.has_submitted_full_manuscript,
            has_set_final_defense_date=navigation_tab.has_set_final_defense_date,
            has_submitted_copyright=navigation_tab.has_submitted_copyright,
        )
        db.add(db_process)
        await db.commit()
        
        await db.refresh(db_process)
        return db_process


    @staticmethod
    async def create_process_role_class_assoc(process_id: str, class_id: str):
        try:
            # Retrieve the navigation record
            navigation_record = await db.execute(select(NavigationTab).where(NavigationTab.id == process_id))
            navigation_record = navigation_record.scalar()

            if not navigation_record:
                raise HTTPException(status_code=404, detail=f"Navigation with id {process_id} not found.")


            navigation_class_entry = NavigationClass(id=str(uuid.uuid4()), navigation_id=process_id, class_id=class_id)
            db.add(navigation_class_entry)
            await db.commit()
            return navigation_class_entry
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")