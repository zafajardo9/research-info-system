from operator import itemgetter
from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, ClassCreate, NavigationTabCreate, ResponseSchema, UpdateAssign, UpdateResearchTypeAssign, UserWithAssignments, WorkflowCreate, WorkflowCreateWithSteps, WorkflowDetail, WorkflowGroupbyType, WorkflowStepCreate, WorkflowStepDetail
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
from app.model.faculty import Faculty
from app.model.workflowprocess import NavigationTab
from app.service.section_service import SectionService

#from app.schema import WorkflowCreate

router = APIRouter(
    prefix="/sections",
    tags=['Getting all for Section'],
    #dependencies=[Depends(JWTBearer())]
)


course_descriptions = {
    "BSIT": "Bachelor of Science in Information Technology",
    "BSENTREP": "Bachelor of Science in Entrepreneurship",
    "BTLEDICT": "Bachelor of Technical and Livelihood Education",
    "BSBAMM": "Bachelor of Science in Business Administration",
    "BBTLEDHE": "Bachelor of Business Technology and Livelihood Education",
    "BSBAHRM": "Bachelor of Science in Business Administration in Human Resource Management",
    "BPAPFM": "Bachelor of Public Administration and Public Finance Management",
    "DOMTMOM": "Doctor of Management and Organizational Management"
}

# @router.get("/course_list")
# async def get_courses():
#     """
#     Get all courses with their descriptions
#     """
#     return course_descriptions

# @router.get("/course_with_year_list")
# async def get_courses():
#     """
#     Mga nasa Table lang for now
#     """
    
#     result = await UsersRepository.filter_student_year_course()
#     if result:
#         return ResponseSchema(detail="Successfully fetch all year and course!", result=result)
#     else:
#         raise HTTPException(status_code=404, detail="No data found")

@router.post("/input-sections/", response_model=List[ClassCreate])
async def create_workflows1(create_data: List[ClassCreate]):

    # Initialize a list to store the created sections
    created_sections = []

    for class_create in create_data:
        # Use the SectionService to check and input the section and course
        created_section = await SectionService.check_and_input_section_course(class_create)
        if created_section:
            created_sections.append(created_section)

    return created_sections


@router.delete("/delete/{id}", response_model=dict)
async def delete_workflow(id: str = Path(..., title="The ID of the Section")):
    deleted = await SectionService.delete_section(id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Section not found")

    return {"message": "Section deleted successfully"}

@router.delete("/delete-all", response_model=dict)
async def delete_workflow():
    deleted = await SectionService.delete_all_section()

    if not deleted:
        raise HTTPException(status_code=404, detail="Section not found")

    return {"message": "All Sections deleted successfully"}

@router.get("/course_with_year_list")
async def get_courses():
    """
    Mga nasa Table lang for now
    """
    
    result = await SectionService.display_all_sections()
    if result:
        return ResponseSchema(detail="Successfully fetch all year and course!", result=result)
    else:
        raise HTTPException(status_code=404, detail="No data found")
