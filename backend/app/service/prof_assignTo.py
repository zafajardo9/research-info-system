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
from app.model import AssignedSectionsToProf
from app.model.users import Users
from app.model.faculty import Faculty

class AssignToProf:
    
  
    
    ####################### FOR RESEARCH PROF ASSIGNING RESEARCH ADVISERS #######################
    
    
    #############################################################################################
    # @staticmethod
    # async def assign_user_researchh_type(assign_data: AssignedResearchTypeCreate):
    #     assign_research_type_id = str(uuid.uuid4()) 
    #     db_assign_research = AssignedResearchTypeToProf(id=assign_research_type_id, **assign_data.dict())
    #     db.add(db_assign_research)
    #     await db.commit()
    #     await db.refresh(db_assign_research)
    #     return db_assign_research
    
    @staticmethod
    async def assign_prof_section(assign_data: AssignedSectionsCreate, user_id: str):
        assign_section_id = str(uuid.uuid4())
        db_assign_section = AssignedSectionsToProf(id=assign_section_id, **assign_data.dict(), user_id=user_id)
        db.add(db_assign_section)
        await db.commit()
        await db.refresh(db_assign_section)
        return db_assign_section
    
    
    #Display the user assign based on the user_id
    # @staticmethod
    # async def display_assignments_by_user(user_id: str):
    #     first_query = select(AssignedResearchTypeToProf).where(AssignedResearchTypeToProf.user_id == user_id)
    #     assigns = await db.execute(first_query)
    #     assigns = assigns.scalars().all()

    #     if not assigns:
    #         return None  # Return None when the workflow is not found

    #     assignments_list = []
    #     for assign in assigns:
    #         second_query = select(AssignedSectionsToProf).where(AssignedSectionsToProf.research_type_id == assign.id)
    #         assign_sections = await db.execute(second_query)
    #         assign_sections = assign_sections.scalars().all()

    #         assign_details = AssignUserProfileNoID(
    #             research_type_name=assign.research_type_name,
    #             assignsection=assign_sections
    #         )
    #         assignments_list.append(assign_details)

    #     return assignments_list
    
    # @staticmethod
    # async def update_research_type_assignment(research_type_id: str, update_data: AssignedResearchTypeCreate):
    #     existing_research_type = await db.get(AssignedResearchTypeToProf, research_type_id)
    #     if not existing_research_type:
    #         return None

    #     for var, value in vars(update_data).items():
    #         if value is not None:
    #             setattr(existing_research_type, var, value)

    #     await db.commit()
    #     return existing_research_type

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
    
    # @staticmethod
    # async def delete_research_type_assignment(research_type_id: str):
        
        
    #     one = delete(AssignedSectionsToProf).where(AssignedSectionsToProf.research_type_id == research_type_id)
    #     await db.execute(one)
    #     two = delete(AssignedResearchTypeToProf).where(AssignedResearchTypeToProf.id == research_type_id)
    #     result = await db.execute(two)
    #     await db.commit()
    #     if result.rowcount == 0:
    #         return False 

    #     return True
        


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
    async def display_assigned_sections(user_id: str):
        try:
            # Fetch assigned sections for the user
            first_query = select(AssignedSectionsToProf).where(AssignedSectionsToProf.user_id == user_id)
            assigns = await db.execute(first_query)
            assigns = assigns.fetchall()

            if not assigns:
                return None  # Return None when no assignments are found

            # Convert SQLAlchemy result to a list of dictionaries
            assignments_list = [dict(assign) for assign in assigns]

            return assignments_list

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
            
    @staticmethod
    async def get_prof_with_assigned():
        try:
            query = (
                select(Users, AssignedSectionsToProf, Faculty)
                .join(Faculty, Users.faculty_id == Faculty.id)
                .join(AssignedSectionsToProf, Users.id == AssignedSectionsToProf.user_id)
            )

            users_with_assignments = await db.execute(query)
            results = users_with_assignments.fetchall()

            # Organize the results as a list of dictionaries with selected fields
            organized_results = []
            current_user = None
            user_data = None

            for row in results:
                if current_user is None or current_user.id != row[0].id:
                    # New user, start a new dictionary
                    if user_data is not None:
                        organized_results.append(user_data)

                    current_user = row[0]
                    user_data = {
                        "id": current_user.id,
                        "username": current_user.username,
                        "email": current_user.email,
                        "faculty_name": None,  # Initialize faculty_name to None
                        "assignments": []
                    }

                    # Check if faculty data is available
                    if row[0].faculty:
                        user_data['faculty_name'] = row[0].faculty.name

                # Add assignment data to the current user's dictionary
                assignment_data = {
                    "section": row[1].section,
                    "course": row[1].course,
                    "id": row[1].id
                }
                user_data['assignments'].append(assignment_data)

            # Add the last user's data to the list
            if user_data is not None:
                organized_results.append(user_data)

            return organized_results

        except Exception as e:
            print(f"Error in get_prof_with_assigned: {e}")
            raise HTTPException(status_code=500, detail=str(e))