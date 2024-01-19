from typing import List, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import distinct
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from app.config import db


from app.service.research_service import ResearchService

from app.repository.users import UsersRepository
from app.schema import ResponseSchema, UpdateAssign


from app.service.users_service import UserService
from app.repository.users import UsersRepository
from app.service.assignTo_service import AssignToSection
from app.model import AssignedSectionsToProf
from app.service.prof_assignTo import AssignToProf
from app.service.faculty_flow import FacultyFlow
from app.service.workflow_service import WorkflowService

router = APIRouter(
    prefix="/show-faculty-process",
    tags=['Just Showing the Process for Faculty (Prof and Advi)'],
    dependencies=[Depends(JWTBearer())]
)


@router.get("/process-of-current-user/")
async def assign_process(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):
    '''
    Process na makikita ng current user base sa role
    '''

    token = JWTRepo.extract_token(credentials)
    user_id = token.get('user_id')

    resultz = await FacultyFlow.overall(user_id)
    return resultz



@router.get("/boolean-process/")
async def process_assigned(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):
    
    token = JWTRepo.extract_token(credentials)
    user_id = token.get('user_id')
    try:
        result = await FacultyFlow.assigned_process_boolean(user_id)
        processed_result = FacultyFlow.process_result(result)
        return processed_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")





# @router.get("/filtered-process-by-user-role/")
# async def filtered_process_by_user_role(credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),):
#     # Get the result from display_process_role
#     token = JWTRepo.extract_token(credentials)
#     user_id = token.get('user_id')

#     user_roles = await UsersRepository.get_user_roles(user_id)

#     if "research professor" in user_roles:
#         assigned_sections = await AssignToProf.display_assigned_sections(user_id)
#         # Fetch NavigationTab data for each section
#         course_section_list = []  # Initialize a list to store course and section values
        
#         for section_data in assigned_sections:
#             assigned_sections_to_prof = section_data['AssignedSectionsToProf']
            
#             course = assigned_sections_to_prof.course
#             section = assigned_sections_to_prof.section

#             # Extracted course and section values
#             course_section_list.append({"course": course, "section": section})

#             navigation_tabs = await FacultyFlow.get_processes_for_user("research professor", course, section)
#             assigned_sections_to_prof.navigation_tabs = navigation_tabs

#         # Construct the response with assigned_sections and course_section_list
#         response_data = {
#             "assigned_sections_as_prof": assigned_sections,
#             "course_section_list": course_section_list
#         }
#     else:
#         assigned_sections = ["Nothing found assign as a research professor"]
#         # Construct the response without course_section_list
#         response_data = {
#             "assigned_sections_as_prof": assigned_sections,
#         }

#     return response_data





@router.get("/filtered-process-by-user-role/")
async def filtered_process_by_user_role(credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),):
    # Get the result from display_process_role
    token = JWTRepo.extract_token(credentials)
    user_id = token.get('user_id')

    user_roles = await UsersRepository.get_user_roles(user_id)
    
    navigation_tabs_list = []
    assigned_sections_adviser = []

    if "research professor" in user_roles:
        assigned_sections = await AssignToProf.display_assigned_sections(user_id)


        for section_data in assigned_sections:
            assigned_sections_to_prof = section_data['AssignedSectionsToProf']

            course = assigned_sections_to_prof.course
            section = assigned_sections_to_prof.section

            navigation_tabs = await FacultyFlow.get_processes_for_user("research professor", course, section)

            if navigation_tabs:
                # Add navigation tabs to the list
                navigation_tabs_list.append({"course": course, "section": section, "navigation_tabs": navigation_tabs})
            else:
                # Display a message if no processes are found for the role, section, and course
                navigation_tabs_list.append({"course": course, "section": section, "navigation_tabs": "No process found for this role"})

    else:
        navigation_tabs_list = ["Nothing found assign as a research professor"]
        
    
    if "research adviser" in user_roles:
        assigned_sections_adviser = await FacultyFlow.display_assignment(user_id)
    else:
        assigned_sections_adviser = ["Nothing found assign as a research adviser"]

    # Construct the response
    response_data = {
        "assigned_sections_as_prof": navigation_tabs_list,
        "assigned_sections_as_adviser": assigned_sections_adviser
    }
    return response_data

