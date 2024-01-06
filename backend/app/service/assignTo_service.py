from datetime import datetime
import logging
import uuid
from sqlalchemy import and_, distinct, insert, join
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
from app.schema import AssignUserProfileNoID, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, AssignedSectionsCreateWithID, AuthorShow, CopyRightResponse, DisplayAllByUser, EthicsResponse, FullManuscriptResponse, ResearchPaperCreate, ResearchPaperResponse, ResearchPaperShow, ResearchPaperWithAuthorsResponse, UpdateAssign
from app.service.users_service import UserService
from app.model import AssignedSections, AssignedResearchType
from app.model.users import Users
from app.model.faculty import Faculty
from app.model.assignedTo import AssignedSectionsToProf
from app.model.student import Class

class AssignToSection:
    
    @staticmethod
    async def check_assigned_research_type(user_id: str, research_type: str):

        query = select(AssignedResearchType).where(AssignedResearchType.user_id == user_id, AssignedResearchType.research_type_name == research_type)

        existing_assignment = await db.execute(query)
        
        if existing_assignment.first():
            raise HTTPException(status_code=400, detail="User already has the assigned research type")

        
    
    
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
    
    
    #UPDATE
    @staticmethod
    async def assign_user_section(assign_data: AssignedSectionsCreate, research_type_id: str, section_id: Optional[str] = None):
        if section_id:
            # Update the existing section
            statement = (
                update(AssignedSections)
                .where(AssignedSections.id == section_id)
                .values(**assign_data.dict(), research_type_id=research_type_id)
                .returning(AssignedSections)
            )
            db_assign_section = await db.execute(statement)
        else:
            # Create a new section
            assign_section_id = str(uuid.uuid4())
            db_assign_section = AssignedSections(id=assign_section_id, **assign_data.dict(), research_type_id=research_type_id)
            db.add(db_assign_section)
            await db.commit()
            await db.refresh(db_assign_section)

        return db_assign_section
    
    
    @staticmethod
    async def update_section(section_id: str, research_type_id: str, new_class_id: str) -> dict:
        # Update the existing section's class_id
        statement = (
            update(AssignedSections)
            .where(AssignedSections.id == section_id)
            .where(AssignedSections.research_type_id == research_type_id)
            .values(class_id=new_class_id)
            .returning(AssignedSections)
        )

        updated_section = await db.execute(statement)
        await db.commit()

        # Convert the SQLAlchemy model to a dictionary
        updated_section_dict = dict(updated_section.first())  # Assuming .first() gets the first result

        return updated_section_dict

    
    # Display the user assign based on the user_id
    @staticmethod
    async def display_assignments_by_user(user_id: str):
        first_query = select(AssignedResearchType).where(AssignedResearchType.user_id == user_id)
        assigns = await db.execute(first_query)
        assigns = assigns.scalars().all()

        if not assigns:
            return None  # Return None when the workflow is not found

        assignments_list = []
        for assign in assigns:
            second_query = (select(
                    AssignedSections.id.label("assignment_id"),
                    AssignedSections.class_id,
                    Class.course,
                    Class.section
                    ).where(AssignedSections.research_type_id == assign.id).outerjoin(Class, AssignedSections.class_id == Class.id)
            )
            assign_sections = await db.execute(second_query)
            assign_sections = assign_sections.fetchall()
            
            print(assign_sections)
            
            assign_details = {
                "assigned_type_id": assign.id   ,
                "research_type_name": assign.research_type_name,
                "assignsection": []
            }
            
            for section in assign_sections:
                assign_details["assignsection"].append({
                    "id": section[0],
                    "class_id": section[1],
                    "course": section[2],
                    "section": section[3]
                })

            assignments_list.append(assign_details)

        return assignments_list
    
    @staticmethod
    async def display_assignments_by_type(research_type: str):
        first_query = select(AssignedResearchType).where(AssignedResearchType.research_type_name == research_type)
        assigns = await db.execute(first_query)
        assigns = assigns.scalars().all()

        if not assigns:
            return None  # Return None when the workflow is not found

        assignments_list = []
        for assign in assigns:
            second_query = select(AssignedSections).where(AssignedSections.research_type_id == assign.id)
            assign_sections = await db.execute(second_query)
            assign_sections = assign_sections.scalars().all()

            assign_details = AssignUserProfileNoID(
                research_type_name=assign.research_type_name,
                assignsection=assign_sections
            )
            assignments_list.append(assign_details)

        return assignments_list
    
    
    # @staticmethod
    # async def update_research_type_assignment(research_type_id: str, update_data: AssignedResearchTypeCreate):
    #     existing_research_type = await db.get(AssignedResearchType, research_type_id)
    #     if not existing_research_type:
    #         return None

    #     for var, value in vars(update_data).items():
    #         if value is not None:
    #             setattr(existing_research_type, var, value)

    #     await db.commit()
    #     return existing_research_type

    # @staticmethod
    # async def update_section_assignment(section_id: str, update_data: AssignedSectionsCreate):
    #     existing_section = await db.get(AssignedSections, section_id)
    #     if not existing_section:
    #         return None

    #     for var, value in vars(update_data).items():
    #         if value is not None:
    #             setattr(existing_section, var, value)

    #     await db.commit()
    #     return existing_section
    
    @staticmethod
    async def delete_research_type_assignment(research_type_id: str):
        
        
        one = delete(AssignedSections).where(AssignedSections.research_type_id == research_type_id)
        await db.execute(one)
        two = delete(AssignedResearchType).where(AssignedResearchType.id == research_type_id)
        result = await db.execute(two)
        await db.commit()
        if result.rowcount == 0:
            return False 

        return True
    
    @staticmethod
    async def delete_user_sections(research_type_id: str):

        one = delete(AssignedSections).where(AssignedSections.research_type_id == research_type_id)
        await db.execute(one)
        await db.commit()
        


    @staticmethod
    async def delete_section_assignment(section_id: str):
        try:
            stmt = delete(AssignedSections).where(AssignedSections.id == section_id)
            print(stmt)  # Check the generated SQL statement
            result = await db.execute(stmt)
            await db.commit()
            return result
        except Exception as e:
            print(f"Error in delete_section_assignment: {e}")
            raise
        
        #asdfasdfasdf
    @staticmethod
    async def delete_all_assignment(user_id: str):
        assigned_research_type = await db.execute(select(AssignedResearchType).where(AssignedResearchType.user_id == user_id))
        assigned_research_type = assigned_research_type.scalar()

        if not assigned_research_type:
            return False

        # Delete linked sections
        delete_sections = AssignedSections.__table__.delete().where(AssignedSections.research_type_id == assigned_research_type.id)
        await db.execute(delete_sections)

        # Delete research type assignment
        await db.delete(assigned_research_type)
        await db.commit()

        return True

    # @staticmethod
    # async def delete_assignment(deleted_data: List[AssignedSectionsCreate], user_id: str):
    #     for data in deleted_data:
    #         # pang query
    #         stmt = select(AssignedSectionsToProf).where(
    #             AssignedSectionsToProf.user_id == user_id,
    #             AssignedSectionsToProf.section == data.section,
    #             AssignedSectionsToProf.course == data.course
    #         )
    #         result = await db.execute(stmt)
    #         db_existing_section = result.scalars().first()

    #         # If the value exists, delete the assignment
    #         if db_existing_section:
    #             await db.delete(db_existing_section)
    #             await db.commit()

    #     return {"message": "Section and Course assignment deleted successfully"}



    # @staticmethod
    # async def get_users_with_assignments():
    #     query = (
    #         select(Users, AssignedResearchType, AssignedSections)
    #         .join(AssignedResearchType, Users.id == AssignedResearchType.user_id, isouter=True)
    #         .join(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id, isouter=True)
    #     )

    #     users_with_assignments = await db.execute(query)

    #     results = {}
    #     for user, research_type, section in users_with_assignments:
    #         user_id = user.id

    #         if research_type is not None:
    #             user_profile = await UserService.getprofile(user_id)

    #             if user_id not in results:
    #                 if user_profile is not None:
    #                     results[user_id] = {
    #                         "user_profile": {
    #                             "id": user_profile.id,
    #                             "username": user_profile.username,
    #                             "email": user_profile.email,
    #                             "name": user_profile.name,
    #                             "birth": user_profile.birth,
    #                             "phone_number": user_profile.phone_number
    #                         },
    #                         "assignments": []
    #                     }

    #             assignment = {
    #                 "id": research_type.id,
    #                 "research_type_name": research_type.research_type_name,
    #                 "assignsection": []
    #             }

    #             if section is not None:
    #                 assignment["assignsection"].append({
    #                     "id": section.id,
    #                     "section": section.section,
    #                     "course": section.course
    #                 })

    #             existing_assignment = next(
    #                 (a for a in results[user_id]["assignments"] if a["research_type_name"] == research_type.research_type_name),
    #                 None
    #             )

    #             if existing_assignment:
    #                 existing_assignment["assignsection"].append({
    #                     "id": section.id,
    #                     "section": section.section,
    #                     "course": section.course
    #                 })
    #             else:
    #                 results[user_id]["assignments"].append(assignment)

    #     final_result = []
    #     for user_data in results.values():
    #         if len(user_data["assignments"]) > 0:
    #             final_result.append({
    #                 "user_profile": user_data["user_profile"],
    #                 "assignments": user_data["assignments"]
    #             })

    #     return final_result

    @staticmethod
    async def get_users_with_assignments():
        query = (
            select(Users, AssignedResearchType, AssignedSections)
            .join(AssignedResearchType, Users.id == AssignedResearchType.user_id, isouter=True)
            .join(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id, isouter=True)
        )

        users_with_assignments = await db.execute(query)

        

        return users_with_assignments


    #=================== DISPLAY ALL PROF WITH THEIR SECTION AND COURSE
    # @staticmethod
    # async def assign_prof_to_section(assign_data: List[AssignedSectionsCreate], user_id: str):
    #     for data in assign_data:
    #         #pang query
    #         stmt = select(AssignedSectionsToProf).where(
    #             AssignedSectionsToProf.user_id == user_id,
    #             AssignedSectionsToProf.section == data.section,
    #             AssignedSectionsToProf.course == data.course
    #         )
    #         result = await db.execute(stmt)
    #         db_existing_section = result.scalars().first()

    #         # If yung value di nag eexist the gagawin or inster
    #         if not db_existing_section:
    #             assign_section_id = str(uuid.uuid4())
    #             db_assign_section = AssignedSectionsToProf(id=assign_section_id, **data.dict(), user_id=user_id)
    #             db.add(db_assign_section)
    #             await db.commit()
    #             await db.refresh(db_assign_section)

    #     return db_assign_section


    # @staticmethod
    # async def delete_assignment(deleted_data: List[AssignedSectionsCreate], user_id: str):
    #     for data in deleted_data:
    #         # pang query
    #         stmt = select(AssignedSectionsToProf).where(
    #             AssignedSectionsToProf.user_id == user_id,
    #             AssignedSectionsToProf.section == data.section,
    #             AssignedSectionsToProf.course == data.course
    #         )
    #         result = await db.execute(stmt)
    #         db_existing_section = result.scalars().first()

    #         # If the value exists, delete the assignment
    #         if db_existing_section:
    #             await db.delete(db_existing_section)
    #             await db.commit()

    #     return {"message": "Section and Course assignment deleted successfully"}
    



    # @staticmethod
    # async def display_assigned_for_prof():
    #     query = (
    #         select(
    #             AssignedSectionsToProf.section,
    #             AssignedSectionsToProf.course,
    #             AssignedSectionsToProf.id.label("section_id"),  # Alias for AssignedSectionsToProf.id
    #             Users.id.label("user_id"),  # Alias for Users.id
    #             Faculty.name
    #         )
    #         .join(Users, Users.id == AssignedSectionsToProf.user_id)
    #         .join(Faculty, Users.faculty_id == Faculty.id)
    #     )
    #     result = await db.execute(query)
    #     assigned_sections = result.fetchall()
    

    #     # Create a list to store the modified results
    #     modified_results = []

    #     for section_info in assigned_sections:
    #         # Create a dictionary for each section_info
    #         section_dict = {
    #             "id": section_info.section_id,
    #             "user_id": section_info.user_id,
    #             "professor_name": section_info.name,
    #             "section": section_info.section,
    #             "course": section_info.course
    #         }
            
    #         modified_results.append(section_dict)

    #     return modified_results
    
    
    
    @staticmethod
    async def student_get_adviser_list(class_id: str):
        query = (
            select(
                Users.faculty_id,
                Faculty.name,
                AssignedResearchType.research_type_name,
                AssignedSections.class_id
            )
            .join(AssignedResearchType, Users.id == AssignedResearchType.user_id)
            .join(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id)
            .join(Faculty, Users.faculty_id == Faculty.id)
            .where(
                (AssignedSections.class_id == class_id)
            )
        )
        users_with_assignments = await db.execute(query)
        results = users_with_assignments.fetchall()

        # Group results by research type
        grouped_results = {}
        for result in results:
            research_type = result['research_type_name']
            if research_type not in grouped_results:
                grouped_results[research_type] = []

            grouped_results[research_type].append({
                "faculty_id": result['faculty_id'],
                "name": result['name'],
                "section": result['section'],
                "course": result['course']
            })

        # Convert the dictionary to the desired format
        final_result = []
        for research_type, advisers in grouped_results.items():
            final_result.append({
                "research_type": research_type,
                "advisers": advisers
            })

        return final_result
    
    
    @staticmethod
    async def student_get_prof_list(class_id: str):
        query = (
            select(
                distinct(Users.faculty_id).label('faculty_id'),
                Faculty.name,
                (Users.id).label('user_id'),
                AssignedSectionsToProf.class_id,
            )
            .join(Faculty, Users.faculty_id == Faculty.id)  
            .where(
                (AssignedSectionsToProf.class_id == class_id)
            )
        )
        users_with_assignments = await db.execute(query)
        results = users_with_assignments.fetchall()

        return results


    @staticmethod
    async def get_list_my_adviser(class_id: str, research_type: str):
        query = (
            select(
                Users.id,
                Faculty.name,
                AssignedResearchType.research_type_name,
                AssignedSections.class_id
            )
            .join(AssignedResearchType, Users.id == AssignedResearchType.user_id)
            .join(AssignedSections, AssignedResearchType.id == AssignedSections.research_type_id)
            .join(Faculty, Users.faculty_id == Faculty.id)
            .where(
                (AssignedSections.class_id == class_id) &
                (AssignedResearchType.research_type_name == research_type)
            )
        )
        users_with_assignments = await db.execute(query)
        results = users_with_assignments.fetchall()


        return results