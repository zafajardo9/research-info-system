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
from app.model.assignedTo import AssignedResearchType, AssignedSections
from app.schema import AssignUserProfileNoID




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
    async def get_processes_for_user(role, course, section):
        query = (
            select(NavigationTab)
            .where(NavigationTab.role == role)
            .where(NavigationTab.section == section)
            .where(NavigationTab.course == course)
        )

        process_info = await db.execute(query)
        process_info = process_info.fetchall()

        return [item.dict() for item in process_info] if process_info else []
    
    
    @staticmethod
    async def display_assignment(user_id: str):
        first_query = select(AssignedResearchType).where(AssignedResearchType.user_id == user_id)
        assigns = await db.execute(first_query)
        assigns = assigns.scalars().all()

        if not assigns:
            return None  # Return None when the workflow is not found

        assignments_list = []
        for assign in assigns:
            second_query = select(AssignedSections).where(AssignedSections.research_type_id == assign.id)
            assign_sections = await db.execute(second_query)
            assign_sections = assign_sections.scalars().all()

            for assign_section in assign_sections:
                course = assign_section.course  # Fix the typo here
                section = assign_section.section
                research_type = assign.research_type_name  # Fix the variable name here

                navigation_tabs = await FacultyFlow.get_processes_for_user_and_type("research adviser", course, section, research_type)

                assignments_list.append({"course": course, "section": section, "research_type": research_type, "navigation_tabs": navigation_tabs})

        return assignments_list
    
    @staticmethod   
    async def get_processes_for_user_and_type(role, course, section, research_type):
        query = (
            select(NavigationTab)
            .where(NavigationTab.role == role)
            .where(NavigationTab.section == section)
            .where(NavigationTab.course == course)
            .where(NavigationTab.type == research_type)
        )

        result = await db.execute(query)
        process_info = result.fetchall()

        if not process_info:
            return []

        # Convert Row objects to dictionaries
        process_info = [dict(row) for row in process_info]

        return process_info