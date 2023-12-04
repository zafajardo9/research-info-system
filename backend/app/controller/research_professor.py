from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, ResponseSchema, UpdateAssign, UserWithAssignments, WorkflowCreate, WorkflowDetail, WorkflowStepCreate, WorkflowStepDetail
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.workflow_repo import WorkflowRepository
from app.repository.workflowsteps_repo import WorkflowStepRepository
from app.model import Workflow, WorkflowStep, AssignedResearchType, AssignedSections
from app.service.workflow_service import WorkflowService
from app.service.assignTo_service import AssignToSection
from app.service.users_service import UserService

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



@router.post("/assign-adviser-type-section/", response_model=AssignedResearchType)
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


@router.put("/user-assignments-update/{user_id}", response_model=AssignWhole)
async def update_user_assignments(
    user_id: str,
    update_data: UpdateAssign,
):
    try:
        user_assignments = await AssignToSection.update_assignments(user_id, update_data)
        if not user_assignments:
            raise HTTPException(status_code=404, detail="User assignments not found")

        return user_assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/user/{user_id}/assignments", response_model=AssignUserProfile)
async def read_user_assignments(user_id: str):
    try:
        # Get user profile
        user_profile = await UserService.get_faculty_profile_by_ID(user_id)
        if user_profile is None:
            raise HTTPException(status_code=404, detail="User profile not found")

        # Get user assignments
        assignments = await AssignToSection.display_assignments_by_user(user_profile["id"])
        if assignments is None:
            raise HTTPException(status_code=404, detail="Assignments not found")

        # Combine user profile and assignments
        response_data = {
            "user_profile": user_profile,
            "assignments": assignments.dict(),
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/users-with-assignments", response_model=List[UserWithAssignments])
async def get_users_with_assignments():
    try:
        users_with_assignments = await AssignToSection.get_users_with_assignments()
        return users_with_assignments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))