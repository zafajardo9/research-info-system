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

from app.repository.assignTo_repo import AssignedResearchTypeRepository, AssignedSectionsRepository
from app.schema import AssignUserProfileNoID, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, AuthorShow, CopyRightResponse, DisplayAllByUser, EthicsResponse, FullManuscriptResponse, ResearchPaperCreate, ResearchPaperResponse, ResearchPaperShow, ResearchPaperWithAuthorsResponse, UpdateAssign
from app.service.users_service import UserService
from app.model import AssignedResearchTypeToProf, AssignedSectionsToProf
from app.model.users import Users
from app.model.faculty import Faculty

class AssignToProf:
    
  
    
    ####################### FOR RESEARCH PROF ASSIGNING RESEARCH ADVISERS #######################
    
    
    #############################################################################################
    @staticmethod
    async def assign_user_researchh_type(assign_data: AssignedResearchTypeCreate):
        assign_research_type_id = str(uuid.uuid4()) 
        db_assign_research = AssignedResearchTypeToProf(id=assign_research_type_id, **assign_data.dict())
        db.add(db_assign_research)
        await db.commit()
        await db.refresh(db_assign_research)
        return db_assign_research
    
    @staticmethod
    async def assign_user_section(assign_data: AssignedSectionsCreate, research_type_id: str):
        assign_section_id = str(uuid.uuid4())
        db_assign_section = AssignedSectionsToProf(id=assign_section_id, **assign_data.dict(), research_type_id=research_type_id)
        db.add(db_assign_section)
        await db.commit()
        await db.refresh(db_assign_section)
        return db_assign_section
    
    
    #Display the user assign based on the user_id
    @staticmethod
    async def display_assignments_by_user(user_id: str):
        first_query = select(AssignedResearchTypeToProf).where(AssignedResearchTypeToProf.user_id == user_id)
        assigns = await db.execute(first_query)
        assigns = assigns.scalars().all()

        if not assigns:
            return None  # Return None when the workflow is not found

        assignments_list = []
        for assign in assigns:
            second_query = select(AssignedSectionsToProf).where(AssignedSectionsToProf.research_type_id == assign.id)
            assign_sections = await db.execute(second_query)
            assign_sections = assign_sections.scalars().all()

            assign_details = AssignUserProfileNoID(
                research_type_name=assign.research_type_name,
                assignsection=assign_sections
            )
            assignments_list.append(assign_details)

        return assignments_list
    
    @staticmethod
    async def update_research_type_assignment(research_type_id: str, update_data: AssignedResearchTypeCreate):
        existing_research_type = await db.get(AssignedResearchTypeToProf, research_type_id)
        if not existing_research_type:
            return None

        for var, value in vars(update_data).items():
            if value is not None:
                setattr(existing_research_type, var, value)

        await db.commit()
        return existing_research_type

    @staticmethod
    async def update_section_assignment(section_id: str, update_data: AssignedSectionsCreate):
        existing_section = await db.get(AssignedSectionsToProf, section_id)
        if not existing_section:
            return None

        for var, value in vars(update_data).items():
            if value is not None:
                setattr(existing_section, var, value)

        await db.commit()
        return existing_section
    
    @staticmethod
    async def delete_research_type_assignment(research_type_id: str):
        
        
        one = delete(AssignedSectionsToProf).where(AssignedSectionsToProf.research_type_id == research_type_id)
        await db.execute(one)
        two = delete(AssignedResearchTypeToProf).where(AssignedResearchTypeToProf.id == research_type_id)
        result = await db.execute(two)
        await db.commit()
        if result.rowcount == 0:
            return False 

        return True
        


    @staticmethod
    async def delete_section_assignment(section_id: str):
        try:
            stmt = delete(AssignedSectionsToProf).where(AssignedSectionsToProf.id == section_id)
            print(stmt)  # Check the generated SQL statement
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            print(f"Error in delete_section_assignment: {e}")
            raise
    
    
    @staticmethod
    async def get_users_with_assignments():
        query = (
            select(Users, AssignedResearchTypeToProf, AssignedSectionsToProf)
            .join(AssignedResearchTypeToProf, Users.id == AssignedResearchTypeToProf.user_id)
            .join(AssignedSectionsToProf, AssignedResearchTypeToProf.id == AssignedSectionsToProf.research_type_id)
        )

        users_with_assignments = await db.execute(query)

        results = {}
        for user, research_type, section in users_with_assignments:
            user_id = user.id

            if user_id not in results:
                # If user not in results, add user profile and initialize assignments list
                user_profile = await UserService.get_faculty_profile_by_ID(user_id)
                results[user_id] = {
                    "user_profile": {
                        "id": user_profile.id,
                        "username": user_profile.username,
                        "email": user_profile.email,
                        "name": user_profile.name,
                        "birth": user_profile.birth,
                        "phone_number": user_profile.phone_number
                    },
                    "assignments": []
                }

            # Add assignment to the user's assignments list
            assignment = {
                "id": research_type.id,
                "research_type_name": research_type.research_type_name,
                "assignsection": [
                    {
                        "id": section.id,
                        "section": section.section,
                        "course": section.course
                    }
                ]
            }

            existing_assignment = next(
                (a for a in results[user_id]["assignments"] if a["research_type_name"] == research_type.research_type_name),
                None
            )

            if existing_assignment:
                existing_assignment["assignsection"].append({
                    "id": section.id,
                    "section": section.section,
                    "course": section.course
                })
            else:
                results[user_id]["assignments"].append(assignment)

        # Convert results to a list with the desired structure
        final_result = []
        for user_data in results.values():
            final_result.append({
                "user_profile": user_data["user_profile"],
                "assignments": user_data["assignments"]
            })

        return final_result