from typing import List, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
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


# @router.get("/filtered-process-by-user-role/")
# async def filtered_process_by_user_role(credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),):
#     # Get the result from display_process_role
    
#     token = JWTRepo.extract_token(credentials)
#     user_id = token.get('user_id')

#     display_process_result = await WorkflowService.display_process()

#     user_roles = await UsersRepository.get_user_roles(user_id)

#     if "research professor" in user_roles:
#         assigned_sections = await AssignToProf.display_assigned_sections(user_id)
        
#     else:
#         assigned_sections = ["Nothing found assign as a research professor"]
        
        
#     if "research adviser" in user_roles:
#         assigned_sections_adviser = await AssignToSection.display_assignments_by_user(user_id)
#     else:
#         assigned_sections_adviser = ["Nothing found assign as a research adviser"]
        
#         # Get the assigned_sections_as_prof
#     assigned_sections_as_prof = [
#         {
#             "AssignedSectionsToProf": {
#                 "course": assigned_section["course"],
#                 "id": assigned_section["id"],
#                 "section": assigned_section["section"],
#                 "user_id": assigned_section["user_id"]
#             }
#         } for assigned_section in assigned_sections if assigned_section["course"] == course
#     ]

#     # Get the assigned_sections_as_adviser
#     assigned_sections_as_adviser = [
#         {
#             "research_type_name": assigned_section_adviser["research_type_name"],
#             "assignsection": assigned_section_adviser["assignsection"]
#         } for assigned_section_adviser in assigned_sections_adviser if assigned_section_adviser["assignsection"][0]["course"] == course
#     ]

#     # Construct the response
#     response_data = {
#         "filtered_results_as_prof": assigned_sections_as_prof,
#         "filtered_results_as_adviser": assigned_sections_as_adviser,
#     }
        

