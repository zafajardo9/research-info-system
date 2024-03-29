from datetime import datetime
import logging
import uuid
from sqlalchemy import and_, func, insert, join
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Optional
from uuid import uuid4
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.assignTo_repo import AssignedResearchTypeRepository, AssignedSectionsRepository
from app.schema import AssignedSectionsCreate
from app.service.users_service import UserService
from app.model import AssignedSectionsToProf
from app.model.users import Users
from app.model.faculty import Faculty
from app.service.section_service import SectionService
from app.model.student import Class
from app.service.assignTo_service import AssignToSection

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
        
        
        #CHECKER para saexist
        existing_assignment = await db.execute(
            select(AssignedSectionsToProf)
            .where(
                (AssignedSectionsToProf.class_id == assign_data.class_id) &
                (AssignedSectionsToProf.user_id == user_id)
            )
        )
        
        existing = existing_assignment.scalar_one_or_none()

        if existing:
            # If the assignment already exists, you can handle it accordingly
            raise HTTPException(status_code=400, detail="Assignment already exists for this class_id")

        assign_section_id = str(uuid.uuid4())
        db_assign_section = AssignedSectionsToProf(id=assign_section_id, **assign_data.dict(), user_id=user_id)
        db.add(db_assign_section)
        await db.commit()
        await db.refresh(db_assign_section)
        return db_assign_section
    
    @staticmethod
    async def assign_sections_to_user(user_id: str, class_assignments: List[AssignedSectionsCreate]):
        user_assigned_sections = []

        for class_assignment in class_assignments:
            try:
                existing_assignment = await db.execute(
                    select(AssignedSectionsToProf)
                    .where(
                        (AssignedSectionsToProf.class_id == class_assignment.class_id) &
                        (AssignedSectionsToProf.user_id == user_id)
                    )
                    .limit(1)
                )
                existing = existing_assignment.scalar_one()

                raise HTTPException(status_code=400, detail=f"Assignment already exists for user {user_id} and class {class_assignment.class_id}")

            except NoResultFound:
                try:
                    assign_section_id = str(uuid.uuid4())
                    db_assign_section = AssignedSectionsToProf(id=assign_section_id, **class_assignment.dict(), user_id=user_id)            
                    db.add(db_assign_section)
                    user_assigned_sections.append(db_assign_section)

                    await db.commit()
                    for db_assign_section in user_assigned_sections:
                        await db.refresh(db_assign_section)

                except HTTPException as e:
                    if "Assignment already exists" not in str(e.detail):
                        raise
        return user_assigned_sections

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
            first_query = select(
                        AssignedSectionsToProf.id, 
                        AssignedSectionsToProf.class_id, 
                        Class.course, 
                        Class.section).join(Class, AssignedSectionsToProf.class_id == Class.id).where(AssignedSectionsToProf.user_id == user_id)
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
    async def kalahatan_ito_prof(user_id: str):
        try:
            # Fetch assigned sections for the user
            first_query = select(
                AssignedSectionsToProf.id,
                AssignedSectionsToProf.class_id,
                Class.course,
                Class.section,
            ).join(Class, AssignedSectionsToProf.class_id == Class.id).where(
                AssignedSectionsToProf.user_id == user_id
            )
            assigns = await db.execute(first_query)
            assigns = assigns.fetchall()

            if not assigns:
                return None  # Return None when no assignments are found

            # Convert SQLAlchemy result to a list of dictionaries
            assignments_list = []

            for assign in assigns:
                process_assigned = await AssignToSection.booleans_prof(assign.class_id, "research professor", )

                assign_details = dict(assign)
                assign_details["process"] = process_assigned
                assignments_list.append(assign_details)

            return assignments_list

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
            
    # @staticmethod
    # async def get_prof_with_assigned():
    #     try:
    #         query = (
    #             select(Users, AssignedSectionsToProf, Faculty)
    #             .join(Faculty, Users.faculty_id == Faculty.id)
    #             .join(AssignedSectionsToProf, Users.id == AssignedSectionsToProf.user_id)
    #         )

    #         users_with_assignments = await db.execute(query)
    #         results = users_with_assignments.fetchall()

    #         organized_results = []
    #         current_user = None

    #         for row in results:
    #             if current_user is None or current_user.id != row[0].id:
    #                 if current_user is not None:
    #                     organized_results.append(UserData(**current_user.dict()))

    #                 current_user = row[0]
    #                 current_user.faculty_name = row[0].faculty.name if row[0].faculty else None
    #                 current_user.assignments = []

    #             assignment_data = AssignmentData(class_id=row[1].class_id, id=row[1].id)

    #             # Get section and course information from the class_id
    #             section_course_info = await SectionService.what_section_course(row[1].class_id)

    #             assignment_data.section = section_course_info.section
    #             assignment_data.course = section_course_info.course

    #             current_user.assignments.append(assignment_data)

    #         if current_user is not None:
    #             organized_results.append(UserData(**current_user.dict()))

    #         response_data = ProfWithAssignedResponse(users=organized_results)
    #         return response_data.dict()

    #     except Exception as e:
    #         print(f"Error in get_prof_with_assigned: {e}")
    #         raise HTTPException(status_code=500, detail=str(e))
    
    
    @staticmethod
    async def get_prof_with_assigned():
        try:
            query = (
                select(
                    Users.id,
                    Users.faculty_id,
                    func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('faculty_name'),
                    AssignedSectionsToProf.class_id,
                    AssignedSectionsToProf.id.label("assigned_id"),
                    Class.section,
                    Class.course
                    
                )
                .join(AssignedSectionsToProf, Users.id == AssignedSectionsToProf.user_id)
                .join(Faculty, Users.faculty_id == Faculty.FacultyId)
                .join(Class, AssignedSectionsToProf.class_id == Class.id)
            )

            users_with_assignments = await db.execute(query)
            results = users_with_assignments.fetchall()

            user_assignments_dict = {}
            
            for result in results:
                user_id, faculty_id, faculty_name, class_id, assigned_id, section, course = result
                
                if user_id not in user_assignments_dict:
                    user_assignments_dict[user_id] = {
                        "Faculty": {
                            "id": user_id,
                            "faculty_id": faculty_id,
                            "faculty_name": faculty_name,
                        },
                        "AssignedTo": []
                    }

                user_assignments_dict[user_id]["AssignedTo"].append({
                    "assigned_id": assigned_id,
                    "class_id": class_id,
                    "course": course,
                    "section": section,
                    
                })

            final_result = list(user_assignments_dict.values())
            
            return final_result

        except Exception as e:
            print(f"Error in get_users_with_assignments: {e}")
            raise HTTPException(status_code=500, detail=str(e))