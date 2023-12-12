from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, ResponseSchema, UpdateAssign, UpdateResearchTypeAssign, UserWithAssignments, WorkflowCreate, WorkflowDetail, WorkflowStepCreate, WorkflowStepDetail
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.workflow_repo import WorkflowRepository
from app.repository.workflowsteps_repo import WorkflowStepRepository
from app.model import Workflow, WorkflowStep, AssignedResearchType, AssignedSections
from app.service.workflow_service import WorkflowService
from app.service.assignTo_service import AssignToSection
from app.service.users_service import UserService
from app.repository.users import UsersRepository
from app.model.users import Users


from app.config import db

#from app.schema import WorkflowCreate

router = APIRouter(
    prefix="/researchprof",
    tags=['Research Professor'],
    dependencies=[Depends(JWTBearer())]
)



@router.post("/workflows/", response_model=Workflow)
async def create_workflow(workflow_data: WorkflowCreate, workflow_steps: List[WorkflowStepCreate], credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    created_workflow = await WorkflowService.create_workflow(workflow_data, current_user)
    for step_data in workflow_steps:
        created_workflow_step = await WorkflowService.create_workflow_step(step_data, created_workflow.id)

    return created_workflow


@router.get("/workflows/user", response_model=List[WorkflowDetail])
async def read_workflow(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])

    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    workflow = await WorkflowService.get_workflow_with_steps(current_user)
    
    print(workflow) # Add this line
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow



@router.get("/workflows/{workflow_id}", response_model=WorkflowDetail)
async def read_workflow_by_id(workflow_id: str = Path(..., title="The ID of the workflow")):
    workflow = await WorkflowService.get_workflow_by_id_with_steps(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow


@router.delete("/workflows/{workflow_id}", response_model=dict)
async def delete_workflow(workflow_id: str = Path(..., title="The ID of the workflow")):
    deleted = await WorkflowService.delete_workflow_by_id(workflow_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return {"message": "Workflow deleted successfully"}

# ==========================ASSIGNING=============================================================


@router.post("/assign-adviser/{user_id}")
async def assign_role(
    user_id: str,

    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    assigned_role = "research adviser"
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign role to the user
    await UsersRepository.assign_role(user_id, assigned_role)

    return {"message": f"Research Adviser assigned to user with ID {user_id}"}

@router.delete("/remove-adviser-role/{user_id}")
async def remove_role(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])
    removed_role = "research adviser"

    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove role from the user
    await UsersRepository.remove_role(user_id, removed_role)

    # Call the delete_all_assignment function after successfully removing the role
    await AssignToSection.delete_all_assignment(user_id)

    return {"message": f"Role removed from user with ID {user_id}"}

# ==================== ASSIGNING ADIVIOSER

# @router.post("/assign-adviser-type-section/", response_model=AssignedResearchType)
# async def assign_section(
#         assign_research_type: AssignedResearchTypeCreate, 
#         assign_section: List[AssignedSectionsCreate], 
#         credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
#     ):
#     token = JWTRepo.extract_token(credentials)
#     roles = token.get('role', [])
#     if "research professor" not in roles:
#         raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

#     assignUser = await AssignToSection.assign_user_researchh_type(assign_research_type)
#     for each in assign_section:
#         assigned_section = await AssignToSection.assign_user_section(each, assignUser.id)

#     return assignUser


@router.post("/assign-adviser-type/", response_model=AssignedResearchType)
async def assign_section(
        assign_research_type: AssignedResearchTypeCreate, 
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

    assignUser = await AssignToSection.assign_user_researchh_type(assign_research_type)

    return assignUser


@router.post("/assign-adviser-section/{research_type_id}", response_model=List[AssignedSectionsCreate])
async def assign_section(
        assign_section: List[AssignedSectionsCreate], 
        research_type_id: str,
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

    assigned_sections = []

    for each in assign_section:
        assigned_section = await AssignToSection.assign_user_section(each, research_type_id)
        assigned_sections.append(assigned_section)

    return assigned_sections

# @router.put("/update-adviser-type-section/{research_type_id}")
# async def update_research_type(research_type_id: str, update_data: AssignedResearchTypeCreate, sections_data: List[AssignedSectionsCreate], credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
#     token = JWTRepo.extract_token(credentials)
#     user_roles = token.get('role', [])

#     if "research professor" not in user_roles:
#         raise HTTPException(status_code=403, detail="Access forbidden. Only Research Professors are allowed.")

#     # Update the research type
#     updated_research_type = await AssignToSection.update_research_type_assignment(research_type_id, update_data)
#     if not updated_research_type:
#         raise HTTPException(status_code=404, detail="Research Type not found")

#     # Update the sections
#     for section_data in sections_data:
#         updated_section = await AssignToSection.update_section_assignment(section_data.id, section_data)
#         if not updated_section:
#             raise HTTPException(status_code=404, detail="Section not found")

#     return {"message": f"Research Type and sections updated successfully"}

@router.delete("/delete-all-assigned/{user_id}")
async def delete_all_assignment(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''
    deleting all assigned 
    Also delete all linkSed sections
    '''
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Research Professors are allowed.")

    # Delete research type assignment
    deleted_research_type = await AssignToSection.delete_all_assignment(user_id)

    if not deleted_research_type:
        raise HTTPException(status_code=404, detail="Research Type not found")

    return {"message": f" User assigned all deleted {user_id}"}



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



    
@router.get("/adviser/{user_id}/assigned", response_model=AssignUserProfile)
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



# @router.get("/adviser-with-assigned")
# async def get_users_with_assignments():
#     try:
#         users_with_assignments = await AssignToSection.get_users_with_assignments()
#         result_list = [dict(row) for row in users_with_assignments]
            
#         return result_list
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

# @router.get("/adviser-with-assigned")
# async def get_users_with_assignments():
#     try:
#             # Fetch all AssignedResearchType and their sections
#             assigned_research_types = await db.execute(select(AssignedResearchType))
#             assigned_research_types = assigned_research_types.scalars().all()

#             # Get profiles for each user in the list
#             result_list = []
#             for assign in assigned_research_types:
#                 # Get sections for the current AssignedResearchType
#                 assign_sections = await db.execute(select(AssignedSections).where(AssignedSections.research_type_id == assign.id))
#                 assign_sections = assign_sections.scalars().all()

#                 # Get user profile using user_id from the current AssignedResearchType
#                 profile = await UserService.getprofile(assign.user_id)

#                 # Create the response structure
#                 assign_details = {
#                     "research_type_id": assign.id,
#                     "research_type_name": assign.research_type_name,
#                     "assign_sections": [
#                         {
#                         "id": section.id,
#                         "section": section.section, 
#                         "course": section.course
#                          } 
                        
#                         for section in assign_sections]
#                 }

#                 result_list.append({"user_profile": profile, "assignments": assign_details})
            
#             return result_list
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.get("/adviser-with-assigned")
async def get_users_with_assignments():
    try:
            # Fetch all AssignedResearchType and their sections
            assigned_research_types = await db.execute(select(AssignedResearchType))
            assigned_research_types = assigned_research_types.scalars().all()

            # Group assignments by user
            user_assignments = {}
            for assign in assigned_research_types:
                if assign.user_id not in user_assignments:
                    user_assignments[assign.user_id] = {
                        "user_profile": await UserService.getprofile(assign.user_id),
                        "assignments": []
                    }
                
                # Get sections for the current AssignedResearchType
                assign_sections = await db.execute(select(AssignedSections).where(AssignedSections.research_type_id == assign.id))
                assign_sections = assign_sections.scalars().all()

                # Create the assignment details
                assign_details = {
                    "research_type_id": assign.id,
                    "research_type_name": assign.research_type_name,
                    "assign_sections": [
                        {
                            "id": section.id,
                            "section": section.section,
                            "course": section.course
                        }
                        for section in assign_sections
                    ]
                }

                user_assignments[assign.user_id]["assignments"].append(assign_details)

            # Convert dictionary values to a list for the final response
            result_list = list(user_assignments.values())
            
            return result_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))