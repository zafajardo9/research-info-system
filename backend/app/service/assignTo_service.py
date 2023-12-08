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
from app.schema import AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, AuthorShow, CopyRightResponse, DisplayAllByUser, EthicsResponse, FullManuscriptResponse, ResearchPaperCreate, ResearchPaperResponse, ResearchPaperShow, ResearchPaperWithAuthorsResponse, UpdateAssign
from app.service.users_service import UserService
from app.model import AssignedSections, AssignedResearchType, AssignedSectionsToProf
from app.model.users import Users
from app.model.faculty import Faculty

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
            select(Users, AssignedResearchType, AssignedSections)
            .join(AssignedResearchType, Users.id == AssignedResearchType.user_id)
            .join(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id)
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
                "research_type_name": research_type.research_type_name,
                "assignsection": {
                    "section": section.section,
                    "course": section.course
                }
            }
            results[user_id]["assignments"].append(assignment)

        return list(results.values())
    
    # =================== DISPLAY ALL PROF WITH THEIR SECTION AND COURSE
    @staticmethod
    async def assign_prof_to_section(assign_data: List[AssignedSectionsCreate], user_id: str):
        for data in assign_data:
            #pang query
            stmt = select(AssignedSectionsToProf).where(
                AssignedSectionsToProf.user_id == user_id,
                AssignedSectionsToProf.section == data.section,
                AssignedSectionsToProf.course == data.course
            )
            result = await db.execute(stmt)
            db_existing_section = result.scalars().first()

            # If yung value di nag eexist the gagawin or inster
            if not db_existing_section:
                assign_section_id = str(uuid.uuid4())
                db_assign_section = AssignedSectionsToProf(id=assign_section_id, **data.dict(), user_id=user_id)
                db.add(db_assign_section)
                await db.commit()
                await db.refresh(db_assign_section)

        return db_assign_section


    @staticmethod
    async def delete_assignment(deleted_data: List[AssignedSectionsCreate], user_id: str):
        for data in deleted_data:
            # pang query
            stmt = select(AssignedSectionsToProf).where(
                AssignedSectionsToProf.user_id == user_id,
                AssignedSectionsToProf.section == data.section,
                AssignedSectionsToProf.course == data.course
            )
            result = await db.execute(stmt)
            db_existing_section = result.scalars().first()

            # If the value exists, delete the assignment
            if db_existing_section:
                await db.delete(db_existing_section)
                await db.commit()

        return {"message": "Section and Course assignment deleted successfully"}


    @staticmethod
    async def display_assigned_for_prof():
        query = (
            select(
                AssignedSectionsToProf.section,
                AssignedSectionsToProf.course,
                AssignedSectionsToProf.id.label("section_id"),  # Alias for AssignedSectionsToProf.id
                Users.id.label("user_id"),  # Alias for Users.id
                Faculty.name
            )
            .join(Users, Users.id == AssignedSectionsToProf.user_id)
            .join(Faculty, Users.faculty_id == Faculty.id)
        )
        result = await db.execute(query)
        assigned_sections = result.fetchall()
    

        # Create a list to store the modified results
        modified_results = []

        for section_info in assigned_sections:
            # Create a dictionary for each section_info
            section_dict = {
                "id": section_info.section_id,
                "user_id": section_info.user_id,
                "professor_name": section_info.name,
                "section": section_info.section,
                "course": section_info.course
            }
            
            modified_results.append(section_dict)

        return modified_results
    
    
    
    @staticmethod
    async def student_get_adviser_list(user_course: str, user_section: str):
        query = (
            select(
                Users.faculty_id,
                Faculty.name,
                AssignedResearchType.research_type_name,
                AssignedSections.section,
                AssignedSections.course
            )
            .join(AssignedResearchType, Users.id == AssignedResearchType.user_id)
            .join(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id)
            .join(Faculty, Users.faculty_id == Faculty.id)  # Join with the Faculty table
            .where(
                (AssignedSections.section == user_section) &
                (AssignedSections.course == user_course)
                # (AssignedResearchType.research_type_name == "")
            )
        )
        users_with_assignments = await db.execute(query)
        results = users_with_assignments.fetchall()
        
        return results
    
    
    @staticmethod
    async def student_get_prof_list(user_course: str, user_section: str):
        query = (
            select(
                Users.faculty_id,
                Faculty.name,
                AssignedSectionsToProf.section,
                AssignedSectionsToProf.course
            )
            .join(AssignedSectionsToProf, Users.id == AssignedSectionsToProf.user_id)
            .join(Faculty, Users.faculty_id == Faculty.id)  # Join with the Faculty table
            .where(
                (AssignedSectionsToProf.section == user_section) &
                (AssignedSectionsToProf.course == user_course)
            )
        )
        users_with_assignments = await db.execute(query)
        results = users_with_assignments.fetchall()
        
        return results