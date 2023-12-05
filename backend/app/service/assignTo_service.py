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

from app.repository.assignTo_repo import AssignedResearchTypeRepository, AssignedSectionsRepository
from app.schema import AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, AuthorShow, CopyRightResponse, DisplayAllByUser, EthicsResponse, FullManuscriptResponse, ResearchPaperCreate, ResearchPaperResponse, ResearchPaperShow, ResearchPaperWithAuthorsResponse, UpdateAssign
from app.service.users_service import UserService
from app.model import AssignedSections, AssignedResearchType
from app.model.users import Users

class AssignToSection:
    
    @staticmethod
    async def assign_user_researchh_type(assign_data: AssignedResearchTypeCreate):
        assign_research_type_id = str(uuid.uuid4()) 
        db_assign_research = AssignedResearchType(id=assign_research_type_id, **assign_data.dict())
        db.add(db_assign_research)
        await db.commit()
        await db.refresh(db_assign_research)
        return db_assign_research
    
    @staticmethod
    async def assign_user_section(assign_data: AssignedSectionsCreate, research_type_id: str):
        assign_section_id = str(uuid.uuid4())
        db_assign_section = AssignedSections(id=assign_section_id, **assign_data.dict(), research_type_id=research_type_id)
        db.add(db_assign_section)
        await db.commit()
        await db.refresh(db_assign_section)
        return db_assign_section
    
    
    #Display the user assign based on the user_id
    @staticmethod
    async def display_assignments_by_user(user_id: str):
        first_query = select(AssignedResearchType).where(AssignedResearchType.user_id == user_id)
        assign = await db.execute(first_query)
        assign = assign.scalar()

        if not assign:
            return None  # Return None when the workflow is not found

        second_query = select(AssignedSections).where(AssignedSections.research_type_id == assign.id)
        assign_section = await db.execute(second_query)
        assign_section = assign_section.scalars().all()

        detail = AssignWhole(
            id=assign.id,
            user_id=assign.user_id,
            research_type_name=assign.research_type_name,
            assignsection=assign_section
        )

        return detail
    

    @staticmethod
    async def update_assignments(user_id: str, update_data: UpdateAssign):
        try:
            # Retrieve existing assignments
            existing_assignments = await AssignToSection.display_assignments_by_user(user_id)
            if not existing_assignments:
                raise HTTPException(status_code=404, detail="User assignments not found")

            # Update existing research type
            research_type_update_data = update_data.assignresearchtype.dict(exclude_unset=True)
            await db.execute(
                update(AssignedResearchType).where(AssignedResearchType.user_id == user_id).values(research_type_update_data)
            )

            # Delete existing sections
            await db.execute(
                delete(AssignedSections).where(AssignedSections.research_type_id == existing_assignments.id)
            )
            assign_section_id = str(uuid.uuid4()) 

    # Insert new sections
            new_sections = [
                {"id": str(uuid.uuid4()), "research_type_id": existing_assignments.id, **section.dict()} 
                for section in update_data.assignsection
            ]
            for section in new_sections:
                await db.execute(insert(AssignedSections).values(section))
            await db.commit()

            # Return updated assignments
            updated_assignments = await AssignToSection.display_assignments_by_user(user_id)
            return updated_assignments
        except Exception as e:
            logging.error(f"Error during update_assignments: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    async def get_users_with_assignments():
        query = (
            select(Users)
            .join(AssignedResearchType, Users.id == AssignedResearchType.user_id)
            .join(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id)
        )
        users_with_assignments = await db.execute(query)

        results = {}
        for user in users_with_assignments.scalars().all():
            user_profile = await UserService.get_faculty_profile_by_ID(user.id)
            
            if user.id not in results:
                assignments = await AssignToSection.display_assignments_by_user(user.id)
                
                results[user.id] = {
                    "user_profile": user_profile,
                    "assignments": assignments.dict(),
                }
            else:
                new_assignment = await AssignToSection.display_assignments_by_user(user.id)
                new_sections = new_assignment.dict()['assignsection']
                
                # If the new section is not already in the list, add it
                for section in new_sections:
                    if section not in results[user.id]['assignments']['assignsection']:
                        results[user.id]['assignments']['assignsection'].append(section)
        
        return list(results.values())