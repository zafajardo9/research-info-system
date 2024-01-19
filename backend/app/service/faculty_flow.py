from datetime import datetime
import uuid
from sqlalchemy import delete, distinct, join, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select
from typing import List, Optional
import uuid
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.model import Users,Faculty , NavigationTab, Role, AssignedResearchType, AssignedSections, AssignedSectionsToProf, Class, NavigationClass, NavigationTab
from app.repository.users import UsersRepository
from app.service.prof_assignTo import AssignToProf
from app.model.assignedTo import AssignedResearchType, AssignedSections
from app.schema import AssignUserProfileNoID
from app.service.assignTo_service import AssignToSection




class FacultyFlow:
    
    @staticmethod
    async def overall(user_id: str):
        
        # Get user roles
        user_roles = await UsersRepository.get_user_roles(user_id)

        if "research professor" in user_roles:
            assigned_sections = await AssignToProf.kalahatan_ito_prof(user_id)
        else:
            assigned_sections = ["Nothing found assign as a research professor"]
        
        
        if "research adviser" in user_roles:
            assigned_sections_adviser = await AssignToSection.kalahatan_ito_adviser(user_id)
            
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
    async def process_assigned(user_id: str):
        
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
    async def assigned_process_boolean(user_id: str):
        query = (
            select(
                distinct(Users.id).label("user_id"),
                AssignedResearchType.id.label("research_type_id"),
                AssignedResearchType.research_type_name,
                Class.id.label("class_id"),
                Class.section,
                Class.course,
                NavigationTab.id.label("navigation_role_id"),
                NavigationTab.role,
                NavigationTab.type,
                NavigationTab.has_submitted_proposal,
                NavigationTab.has_pre_oral_defense_date,
                NavigationTab.has_submitted_ethics_protocol,
                NavigationTab.has_submitted_full_manuscript,
                NavigationTab.has_set_final_defense_date,
                NavigationTab.has_submitted_copyright,
            )
            .select_from(Users)
            .join(AssignedResearchType, Users.id == AssignedResearchType.user_id)
            .outerjoin(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id)
            .outerjoin(Class, AssignedSections.class_id == Class.id)
            .outerjoin(NavigationClass, Class.id == NavigationClass.class_id)
            .outerjoin(NavigationTab, NavigationClass.navigation_id == NavigationTab.id)
            .filter(Users.id == user_id)
        )
        
        result = await db.execute(query)
        result = result.fetchall()
        
        return result
    
    
    
    # @staticmethod
    # async def booleans(class_id: str, role: str):
    #     query = (
    #         select(
    #             NavigationTab.id.label("navigation_role_id"),
    #             NavigationTab.role,
    #             NavigationTab.type,
    #             NavigationTab.has_submitted_proposal,
    #             NavigationTab.has_pre_oral_defense_date,
    #             NavigationTab.has_submitted_ethics_protocol,
    #             NavigationTab.has_submitted_full_manuscript,
    #             NavigationTab.has_set_final_defense_date,
    #             NavigationTab.has_submitted_copyright,
    #         )
    #         .select_from(Users)
    #         .join(AssignedResearchType, Users.id == AssignedResearchType.user_id)
    #         .outerjoin(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id)
    #         .outerjoin(Class, AssignedSections.class_id == Class.id)
    #         .outerjoin(NavigationClass, Class.id == NavigationClass.class_id)
    #         .outerjoin(NavigationTab, NavigationClass.navigation_id == NavigationTab.id)
    #         .filter((NavigationClass.class_id == class_id) & (NavigationTab.role == role))
    #     )

    #     result = await db.execute(query)
    #     result = result.fetchall()

    #     return result
    
    
    @staticmethod
    def process_result(result: List[dict]) -> List[dict]:
        processed_result = []

        for record in result:
            assigned_type_id = record["research_type_id"]
            research_type_name = record["research_type_name"]
            class_id = record["class_id"]
            section = record["section"]
            course = record["course"]
            navigation_role_id = record["navigation_role_id"]
            role = record["role"]
            process_info = {
                "id": navigation_role_id,
                "role": role,
                "type": record["type"],
                "has_submitted_proposal": record["has_submitted_proposal"],
                "has_pre_oral_defense_date": record["has_pre_oral_defense_date"],
                "has_submitted_ethics_protocol": record["has_submitted_ethics_protocol"],
                "has_submitted_full_manuscript": record["has_submitted_full_manuscript"],
                "has_set_final_defense_date": record["has_set_final_defense_date"],
                "has_submitted_copyright": record["has_submitted_copyright"],
            }

            # Check if the assigned_type_id is already in processed_result
            assigned_type_exists = next(
                (
                    item
                    for item in processed_result
                    if item["assigned_type_id"] == assigned_type_id
                ),
                None,
            )

            if assigned_type_exists:
                # If assigned_type_id already exists, append the process_info to the existing section
                existing_section = next(
                    (
                        section
                        for section in assigned_type_exists["assignsection"]
                        if section["id"] == class_id
                    ),
                    None,
                )
                if existing_section:
                    existing_section["process"].append(process_info)
                else:
                    # If section does not exist, create a new section
                    assigned_type_exists["assignsection"].append(
                        {
                            "id": class_id,
                            "course": course,
                            "section": section,
                            "process": [process_info],
                        }
                    )
            else:
                # If assigned_type_id does not exist, create a new entry
                processed_result.append(
                    {
                        "assigned_type_id": assigned_type_id,
                        "research_type_name": research_type_name,
                        "assignsection": [
                            {
                                "id": class_id,
                                "course": course,
                                "section": section,
                                "process": [process_info],
                            }
                        ],
                    }
                )

        return processed_result
    
    
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