from typing import List, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.service.research_service import ResearchService
from app.config import db
from app.repository.users import UsersRepository
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, ResponseSchema, UpdateAssign


from app.service.users_service import UserService
from app.repository.users import UsersRepository
from app.service.assignTo_service import AssignToSection
from app.model import AssignedResearchTypeToProf, AssignedSectionsToProf

router = APIRouter(
    prefix="/admin",
    tags=['Admin Power'],
    dependencies=[Depends(JWTBearer())]
)

@router.post("/assign-roles/{user_id}")
async def assign_roles(
    user_id: str,
    assigned_roles: List[str],
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):

    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign roles to the user
    await UsersRepository.assign_roles(user_id, assigned_roles)

    return {"message": f"Roles assigned to user with ID {user_id}"}



@router.get("/users_faculty_with_roles", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_users_with_roles(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    """
    Get all users with their roles
    """
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")

    result = await UserService.get_all_in_faculty_with_roles()
    
    if result:
        formatted_result = UserService.format_users_with_roles(result)
        return ResponseSchema(detail="Successfully fetched user profiles with roles!", result=formatted_result)
    else:
        raise HTTPException(status_code=404, detail="User list not found")
    
    
    #############################
    
    
    #FOR ASSIGNING
    #############################

# ORIGINAL CODE FROM TOP
@router.post("/assign-professor/{user_id}")
async def assign_roles(
    user_id: str,
    assigned_roles: List[str],
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''
    Assign a User to be a Research Professor
    '''

    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign roles to the user
    await UsersRepository.assign_roles(user_id, assigned_roles)

    return {"message": f"Research Professor assigned to user with ID {user_id}"}


@router.post("/assign-professor-type-section/", response_model=AssignedResearchTypeToProf)
async def assign_section(
        assign_research_type: AssignedResearchTypeCreate, 
        assign_section: List[AssignedSectionsCreate], 
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

    assignUser = await AssignToSection.assign_user_researchh_type(assign_research_type)
    for each in assign_section:
        assigned_section = await AssignToSection.assign_user_section(each, assignUser.id)

    return assignUser


@router.delete("/delete-assigned-research-type/{research_type_id}")
async def delete_assignment(
    research_type_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''
    deleting the research type assigned to adviser
    Also delete all linked sections
    '''
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Research Professors are allowed.")

    # Delete research type assignment
    deleted_research_type = await AssignToSection.delete_research_type_assignment(research_type_id)

    if not deleted_research_type:
        raise HTTPException(status_code=404, detail="Research Type not found")

    return {"message": f"Research type assignment deleted {research_type_id}"}

@router.delete("/delete-assigned-sections/{section_id}")
async def delete_assignment(
    section_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Research Professors are allowed.")

    # Delete section and course assignment
    try:
        deleted_section = await AssignToSection.delete_section_assignment(section_id)
        if deleted_section is None:
            raise HTTPException(status_code=404, detail="Section not found")
        return {"message": f"Section assignment deleted {section_id}"}
    except Exception as e:
        print(f"Error deleting section assignment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/add-section-to-research-assign/{research_type_id}", response_model=List[AssignedSectionsCreate])
async def assign_section(
    assign_section: List[AssignedSectionsCreate], 
    research_type_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):

    '''
    Once nag delete nung mga section and course pwede naman magdagdag pero need ikabit si research type id
    and need din si user id
    '''
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])
    if "research professor" not in roles:
       raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

    assigned_sections = []
    for each in assign_section:
        assigned_section = await AssignToSection.assign_user_section(each, research_type_id)
        assigned_sections.append(assigned_section)

    return assigned_sections



    
@router.get("/professor/{user_id}/assigned", response_model=AssignUserProfile)
async def read_user_assignments(user_id: str):
    try:
        # Get user profile
        user_profile = await UserService.get_faculty_profile_by_ID(user_id)
        if user_profile is None:
            raise HTTPException(status_code=404, detail="User profile not found")

        # Get user assignments
        assignments = await AssignToSection.display_assignments_by_user(user_id)
        if assignments is None:
            raise HTTPException(status_code=404, detail="Assignments not found")

        # Combine user profile and assignments
        response_data = {
            "user_profile": user_profile,
            "assignments": assignments,
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/prof-with-assigned")
async def get_users_with_assignments():
    try:
        users_with_assignments = await AssignToSection.get_users_with_assignments()
        return users_with_assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


