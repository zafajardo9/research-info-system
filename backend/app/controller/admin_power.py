from typing import List, Optional, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.service.research_service import ResearchService
from app.config import db
from app.repository.users import UsersRepository
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, AssignedSectionsWhole, ChangeFacultyPaperStatus, ResponseSchema, UpdateAssign


from app.service.users_service import UserService
from app.repository.users import UsersRepository
from app.service.assignTo_service import AssignToSection
from app.model import AssignedSectionsToProf
from app.service.prof_assignTo import AssignToProf
from app.service.notif_service import NotificationService
from app.model.research_paper import FacultyResearchPaper
from app.repository.research_repo import ResearchPaperRepository

router = APIRouter(
    prefix="/admin",
    tags=['Admin Power'],
    dependencies=[Depends(JWTBearer())]
)


@router.post("/assign-admin/{user_id}")
async def assign_roles(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''
    Assign a User to be a Admin
    '''

    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])
    assigned_role = "admin"

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign role to the user
    if await UsersRepository.has_role(user_id, assigned_role):
        return {"message": f"User with ID {user_id} already has the assigned role."}

        # Assign role to the user
    await UsersRepository.assign_role(user_id, assigned_role)
    await NotificationService.create_notif(user_id, "You have been assigned as a Research Head/Admin")

    return {"message": f"Admin assigned to user with ID {user_id}"}

@router.delete("/remove-admin-role/{user_id}")
async def remove_role(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):

    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])
    removed_role = "admin"

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove role from the user
    await UsersRepository.remove_role(user_id, removed_role)
    await NotificationService.create_notif(user_id, "You have been removed as a Research Head/Admin")

    return {"message": f"Role removed from user with ID {user_id}"}


# ASSIGNING RESEACH PROF AREA =======================================================================
#=============================
@router.post("/assign-research-professor/{user_id}")
async def assign_role(
    user_id: str,

    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    assigned_role = "research professor"
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign role to the user
    if await UsersRepository.has_role(user_id, assigned_role):
        return {"message": f"User with ID {user_id} already has the assigned role."}

        # Assign role to the user
    await UsersRepository.assign_role(user_id, assigned_role)
    await NotificationService.create_notif(user_id, "You have been assigned as a Research Professor")

    return {"message": f"Role assigned to user with ID {user_id}"}

@router.delete("/remove-professor-role/{user_id}")
async def remove_role(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):

    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])
    removed_role = "research professor"

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove role from the user
    await UsersRepository.remove_role(user_id, removed_role)
    await NotificationService.create_notif(user_id, "You have been removed as a Research Professor")

    return {"message": f"Role removed from user with ID {user_id}"}

@router.post("/assign-faculty/{user_id}")
async def assign_roles(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''
    Assign a User to be a Research Professor
    '''

    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])
    assigned_role = "faculty"

    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign role to the user
    if await UsersRepository.has_role(user_id, assigned_role):
        return {"message": f"User with ID {user_id} already has the assigned role."}

        # Assign role to the user
    await UsersRepository.assign_role(user_id, assigned_role)

    return {"message": f"Faculty assigned to user with ID {user_id}"}

@router.delete("/remove-faculty-role/{user_id}")
async def remove_role(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):

    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])
    removed_role = "faculty"

    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove role from the user
    await UsersRepository.remove_role(user_id, removed_role)

    return {"message": f"Role removed from user with ID {user_id}"}



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



@router.post("/assign-section/{user_id}", response_model=List[AssignedSectionsCreate])
async def assign_section(
    assign_section: List[AssignedSectionsCreate], 
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):

    '''
    Assign section
    '''
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

    assigned_sections = []
    for each in assign_section:
        assigned_section = await AssignToProf.assign_prof_section(each, user_id)
        assigned_sections.append(assigned_section)

    return assigned_sections


@router.post("/assign-sections", response_model=List[AssignedSectionsCreate])
async def assign_sections(assignments: List[AssignedSectionsWhole]):
    """
    Assign sections to multiple users.
    """
    assigned_sections = []

    for assignment in assignments:
        user_id = assignment.user_id
        class_assignments = assignment.class_id
        user_assigned_sections = await AssignToProf.assign_sections_to_user(user_id, class_assignments)
        assigned_sections.extend(user_assigned_sections)

    return assigned_sections

@router.delete("/delete-assigned-sections/{assigned_id}")
async def delete_assignment(
    assigned_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Research Professors are allowed.")

    # Delete section and course assignment
    try:
        deleted_section = await AssignToProf.delete_section_assignment(assigned_id)
        if deleted_section is None:
            raise HTTPException(status_code=404, detail="Section not found")
        return {"message": f"Section assignment deleted {assigned_id}"}
    except Exception as e:
        print(f"Error deleting section assignment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    
@router.get("/professor/{user_id}/assigned")
async def read_user_assignments(user_id: str):
    try:
        # Get user profile
        user_profile = await UserService.get_faculty_profile_by_ID(user_id)
        if user_profile is None:
            raise HTTPException(status_code=404, detail="User profile not found")

        # Get user assignments
        assignments = await AssignToProf.display_assigned_sections(user_id)
        if assignments is None:
            raise HTTPException(status_code=404, detail="Assignments not found")

        # Combine user profile and assignments into the expected structure
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
        users_with_assignments = await AssignToProf.get_prof_with_assigned()
        return users_with_assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

@router.get("/view-proposals/list")
async def view_proposal(type: str):
    try:
        users_with_assignments = await ResearchService.view_proposal(type)
        return users_with_assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/view-ethics/list")
async def view_ethics(type: str):
    try:
        users_with_assignments = await ResearchService.view_ethics(type)
        return users_with_assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
        
@router.get("/view-copyright/list")
async def view_copyright(type: str):
    try:
        users_with_assignments = await ResearchService.view_copyright(type)
        return users_with_assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    

    
@router.get("/view-full-manuscript/list")
async def view_manuscript(type: str):
    try:
        users_with_assignments = await ResearchService.view_manuscript(type)
        return users_with_assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.get("/faculty-paper-view/{research_paper_id}", response_model=Optional[FacultyResearchPaper], response_model_exclude_none=True)
async def get_faculty_research_papers(
    research_paper_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)

    try:
        research_papers = await ResearchService.get_faculty_research_papers_by_id(research_paper_id)
        if research_papers:
            return research_papers
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)
    




@router.put("/approve-faculty-paper/{research_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    id: str,
    make_extension: ChangeFacultyPaperStatus,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']  # this line will show what role the logged-in user is

    user_roles = await UsersRepository.get_user_roles(current_user)
    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail=f"You are not allowed to use this feature")

    try:
        research_paper = await ResearchPaperRepository.faculty_paper_approve(db, id, make_extension)
        return ResponseSchema(detail=f"Faculty paper {research_paper.id} is Approved", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error making research extension: {str(e)}", result=None)
    
    
    
