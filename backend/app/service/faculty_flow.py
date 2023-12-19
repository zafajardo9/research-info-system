from datetime import datetime
import uuid
from sqlalchemy import delete, join, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select
from typing import List, Optional
import uuid
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.model import Users,Faculty , NavigationTab, Role
from app.repository.users import UsersRepository
from app.service.assignTo_service import AssignToSection
from app.service.prof_assignTo import AssignToProf




class FacultyFlow:
    
    @staticmethod
    async def overall(user_id: str):
        
        # Get user roles
        user_roles = await UsersRepository.get_user_roles(user_id)

        if "research professor" in user_roles:
            assigned_sections = await AssignToProf.display_assigned_sections(user_id)
        else:
            assigned_sections = ["Nothing found assign as a research professor"]
        
        
        if "research adviser" in user_roles:
            assigned_sections_adviser = await AssignToSection.display_assignments_by_user(user_id)
        else:
            assigned_sections_adviser = ["Nothing found assign as a research adviser"]
        

        # Construct the response
        response_data = {
            "role": user_roles,
            "assigned_sections_as_prof": assigned_sections,
            "assigned_sections_as_adviser": assigned_sections_adviser
            
        }
        
        return response_data
    
    
    @staticmethod
    async def display_process_based_current_user(role: str):
        
        role = await db.execute(select(NavigationTab).where(Role.role_name == role))
        role = role.scalar_one_or_none()
    
    
    @staticmethod   
    async def get_processes_for_user(role, section, course):
        query = (
            select(NavigationTab)
            .where(NavigationTab.role == role)
            .where(NavigationTab.section == section)
            .where(NavigationTab.course == course)
        )

        process_info = await db.execute(query)
        process_info = process_info.fetchone()

        return process_info.dict() if process_info else {}
