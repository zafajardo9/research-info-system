from operator import itemgetter
from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, NavigationTabCreate, ResponseSchema
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
from app.model.student import Class
from app.service.research_service import ResearchService

#from app.schema import WorkflowCreate

router = APIRouter(
    prefix="/researchprof",
    tags=['Research Professor'],
    dependencies=[Depends(JWTBearer())]
)

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



@router.post("/assign-adviser-section/{research_type_id}/", response_model=List[AssignedSectionsCreate])
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


# SA totoo di need dito user_id.. kinuha ko lang talaga

@router.put("/update-assign-adviser-section/{research_type_id}/{section_id}")
async def update_assign_section(
        section_id: str,
        research_type_id: str,
        new_class_id: str,
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract and validate user roles from JWT token
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])
    
    # Check if the user has the required role
    if "research professor" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

    # Call the service function to update the section
    updated_section_dict = await AssignToSection.update_section(section_id, research_type_id, new_class_id)

    # Return the response as per the AssignedSectionsCreate model
    return updated_section_dict

    
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




# todo babalikan
@router.get("/adviser/{user_id}/assigned")
async def read_user_assignments(user_id: str):
    try:
        # Get user profile
        user_profile = await UserService.faculty_info_needed(user_id)
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



# dfgdf

@router.get("/adviser/{research_type}/list")
async def display_by_filter(research_type: str):
    
    try:
            # Fetch all AssignedResearchType and their sections
            assigned_research_types = await db.execute(select(AssignedResearchType).where(AssignedResearchType.research_type_name == research_type))
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
                assign_sections = await db.execute(select(
                    AssignedSections.id.label("assignment_id"),
                    AssignedSections.class_id,
                    Class.course,
                    Class.section
                    ).where(AssignedSections.research_type_id == assign.id).outerjoin(Class, AssignedSections.class_id == Class.id))
                assign_sections = assign_sections.fetchall()
                

                # Create the assignment details
                assign_details = {
                    "research_type_id": assign.id,
                    "research_type_name": assign.research_type_name,
                    "assign_sections": [
                        {
                            "id": assignment_id,
                            "class_id": class_id,
                            "course": course,
                            "section": section
                        }
                        for assignment_id, class_id, course, section in assign_sections
                    ]
                }

                user_assignments[assign.user_id]["assignments"].append(assign_details)

            # Convert dictionary values to a list for the final response
            result_list = list(user_assignments.values())
            
            return result_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# todo FIX
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
                assign_sections = await db.execute(select(
                    AssignedSections.id.label("assignment_id"),
                    AssignedSections.class_id,
                    Class.course,
                    Class.section
                    ).where(AssignedSections.research_type_id == assign.id).outerjoin(Class, AssignedSections.class_id == Class.id))
                assign_sections = assign_sections.fetchall()
                

                # Create the assignment details
                assign_details = {
                    "research_type_id": assign.id,
                    "research_type_name": assign.research_type_name,
                    "assign_sections": [
                        {
                            "id": assignment_id,
                            "class_id": class_id,
                            "course": course,
                            "section": section
                        }
                        for assignment_id, class_id, course, section in assign_sections
                    ]
                }

                user_assignments[assign.user_id]["assignments"].append(assign_details)

            # Convert dictionary values to a list for the final response
            result_list = list(user_assignments.values())
            
            return result_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
# AS A RESEACH PROF NAMAN para makita:
@router.get("/prof/proposal/{course}/{year}",)
async def get_research_papers_by_prof(
    research_type: str,
    course: str,
    year: str):

    try:
        research_papers = await ResearchService.get_research_papers_by_prof(db, research_type, course, year)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "research_type": paper.research_type,
                "status": paper.status
            }
            for paper in research_papers
        ]

        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)



@router.get("/adviser/defense/{course}/{year}",)
async def get_user_research_papers(
    defense_type: str,
    research_type: str,
    course: str,
    year: str):
    '''
        ADVISER lang talaga
    '''

    try:
        research_papers = await ResearchService.get_research_defense_by_adviser(db, research_type, course, year, defense_type)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "time": paper.research_type,
                "date": paper.status
            }
            for paper in research_papers
        ]

        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)


@router.get("/prof/ethics/{course}/{year}")
async def get_research_ethics_by_prof(
    research_type: str,
    course: str,
    year: str):

    try:
        research_papers = await ResearchService.get_research_ethics_by_prof(db, course, year)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Ethics not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "status": paper.status
            }
            for paper in research_papers
        ]
        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user ethics papers: {str(e)}", result=None)
    
    
@router.get("/prof/copyright/{course}/{year}")
async def get_research_copyright_by_prof(
    research_type: str,
    course: str,
    year: str):

    try:
        research_papers = await ResearchService.get_research_copyright_by_prof(db, course, year)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Ethics not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "status": paper.status
            }
            for paper in research_papers
        ]
        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user ethics papers: {str(e)}", result=None)
    

@router.get("/prof/manuscript/{course}/{year}")
async def get_research_manu_by_prof(
    research_type: str,
    course: str,
    year: str):

    try:
        research_papers = await ResearchService.get_research_manu_by_prof(db, course, year)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Ethics not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "status": paper.status
            }
            for paper in research_papers
        ]
        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user ethics papers: {str(e)}", result=None)
    