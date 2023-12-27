from operator import itemgetter
from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, NavigationTabCreate
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.model import AssignedResearchType, AssignedSections
from app.service.workflow_service import WorkflowService
from app.service.assignTo_service import AssignToSection
from app.service.users_service import UserService
from app.repository.users import UsersRepository
from app.model.users import Users
from itertools import groupby


from app.config import db
from app.model.faculty import Faculty
from app.model.workflowprocess import NavigationTab

#from app.schema import WorkflowCreate

router = APIRouter(
    prefix="/researchprof",
    tags=['Research Professor'],
    dependencies=[Depends(JWTBearer())]
)


# ==========================PROCESS NAVIGATION FOR ADVISER AND PROFESSOR=============================================================

faculty_process_name = {
    1 : "Submitted Proposal",
    2 : "Pre-Oral Defense Date",
    3 : "Submitted Ethics/Protocol",
    4 : "Submitted Full Manuscript",
    5 : "Set Final Defense Date",
    6 : "Submitted Copyright"
}


@router.get("/process-list-name")
async def list_of_process_for_faculty():
    '''Can be use in dropdown list'''
    return faculty_process_name

@router.post("/assign-process/")
async def create_process_role(navigation_tab: NavigationTabCreate,):
    create_process = await WorkflowService.create_process_role(navigation_tab)
    return create_process


@router.put("/update-assigned-process/{id}")
async def update_process_role(id: str, navigation_tab: NavigationTabCreate):
    updated_process = await WorkflowService.update_process_role(id, navigation_tab)
    return updated_process

@router.delete("/delete-assigned-process/{id}")
async def update_process_role(id: str):
    delete = await WorkflowService.delete_process_by_id(id)
    if not delete:
        raise HTTPException(status_code=404, detail="Process not found")

    return {"message": "Process deleted successfully"}

    
@router.get("/display-all/")
async def display_process_all():
    '''Wala to like as in same lang nung query sa Database SELECT * FROM'''
    results = await WorkflowService.display_process()
    return results
    
@router.get("/display-process-all/type")
async def display_process_by_type():
    '''Ito may Format pero pwede ka mag req ano pinakamaganda'''
    results = await WorkflowService.display_process_by_type()
    return results

# @router.get("/display-process-all/user_role")
# async def display_process_role():
#     '''Ito may Format pero pwede ka mag req ano pinakamaganda'''
#     results = await WorkflowService.display_process()
#     grouped_results = group_by_role(results)
#     return grouped_results

# def group_by_type(results):
#     # Sort the results by type and section
#     sorted_results = sorted(results, key=lambda x: (x.type, x.section))

#     # Group the sorted results by type
#     grouped_results = {}
#     for research_type, type_group in groupby(sorted_results, key=lambda x: x.type):
#         type_list = list(type_group)
#         grouped_results[research_type] = type_list

#     return grouped_results

# def group_by_role(results):
#     # Sort the results by role and section
#     sorted_results = sorted(results, key=lambda x: (x.role, x.section))

#     # Group the sorted results by role
#     grouped_results = {}
#     for role, role_group in groupby(sorted_results, key=lambda x: x.role):
#         role_list = list(role_group)
#         grouped_results[role] = role_list

#     return grouped_results

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
    if await UsersRepository.has_role(user_id, assigned_role):
        return {"message": f"User with ID {user_id} already has the assigned role."}

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



@router.post("/assign-adviser-type/", response_model=AssignedResearchType)
async def assign_section(
        assign_research_type: AssignedResearchTypeCreate, 
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

    # Check if the user already has the assigned research type
    await AssignToSection.check_assigned_research_type(assign_research_type.user_id, assign_research_type.research_type_name)


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

#asadfasdfasdf

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


# dfgdf

@router.get("/adviser/{research_type}/list")
async def display_by_filter(research_type: str):
    
    query = (select(AssignedResearchType)
            .filter(AssignedResearchType.research_type_name == research_type))
    
    assigned_research_types = await db.execute(query)
    assigned_research_types = assigned_research_types.scalars().all()

    result = []
    for assigned_research_type in assigned_research_types:
        user_profile = await UserService.getprofile(assigned_research_type.user_id)
        
        # Query the AssignedSections table to get the list of assigned sections
        sections_query = (select(AssignedSections)
                        .filter(AssignedSections.research_type_id == assigned_research_type.id))
        assigned_sections = await db.execute(sections_query)
        assigned_sections = assigned_sections.scalars().all()
        
        # Create a new dictionary that only includes the fields you want
        assigned_research_type_dict = {k: v for k, v in vars(assigned_research_type).items() if k != 'user_id'}
        
        result.append({
            "assigned_research_type": assigned_research_type_dict,
            "user_profile": user_profile,
            "assigned_sections": [{"id": section.id, "course": section.course, "section": section.section} for section in assigned_sections]
        })
    
    return result


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