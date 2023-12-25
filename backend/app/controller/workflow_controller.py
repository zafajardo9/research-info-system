from operator import itemgetter
from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, NavigationTabCreate, ResponseSchema, UpdateAssign, UpdateResearchTypeAssign, UserWithAssignments, WorkflowCreate, WorkflowCreateWithSteps, WorkflowDetail, WorkflowStepCreate, WorkflowStepDetail
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.workflow_repo import WorkflowRepository
from app.repository.workflowsteps_repo import WorkflowStepRepository
from app.model import Workflow, WorkflowStep, AssignedResearchType, AssignedSections
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
    prefix="/workflow",
    tags=['Creating workflow (process) for Student'],
    dependencies=[Depends(JWTBearer())]
)

student_process_name = {
    "Proposal": "Proposal",
    "Pre-Oral Defense": "Pre-Oral Defense Date",
    "Ethics": "Ethics/Protocol",
    "Full Manuscript": "Full Manuscript",
    "Final Defense": "Final Defense",
    "Copyright": "Copyright"
}


@router.get("/workflows-list-name-process-student")
async def list_of_process_for_student():
    '''Can be use in dropdown list'''
    return student_process_name



@router.post("/create/1", response_model=List[Workflow])
async def create_workflows1(workflows_data: List[WorkflowCreateWithSteps], credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    created_workflows = []

    for workflow_data_with_steps in workflows_data:
        workflow_data = workflow_data_with_steps.workflow_data
        workflow_steps_data = workflow_data_with_steps.workflow_steps
        
    # Check if workflow already exists
        if await WorkflowService.check_if_workflow_exists(workflow_data.type, workflow_data.year, workflow_data.course):
            raise HTTPException(status_code=400, detail="A workflow with the same type, section, and course already exists.")


        created_workflow = await WorkflowService.create_workflow(workflow_data, current_user)

        for step_data in workflow_steps_data:
            created_workflow_step = await WorkflowService.create_workflow_step(step_data, created_workflow.id)

        created_workflows.append(created_workflow)

    return created_workflows


@router.post("/create/2", response_model=List[Workflow])
async def create_workflows2(workflow_data: List[WorkflowCreate], workflow_steps: List[WorkflowStepCreate], credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    created_workflows = []
    for data in workflow_data:
        
        if await WorkflowService.check_if_workflow_exists(data.type, data.year, data.course):
            raise HTTPException(status_code=400, detail="A workflow with the same type, section, and course already exists.")
        
        
        created_workflow = await WorkflowService.create_workflow(data, current_user)

        for step_data in workflow_steps:
            created_workflow_step = await WorkflowService.create_workflow_step(step_data, created_workflow.id)

        created_workflows.append(created_workflow)

    return created_workflows

#==========================UPDATE

@router.put("/update/{workflow_id}")
async def update_workflow_with_steps(
    workflow_id: str,
    workflow_data: WorkflowCreate,
    steps_data: List[WorkflowStepCreate],
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''Nangyare dito sa update is get the workflow, then ma uupdate tapos si step delete muna lahat then insert new one'''
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to update workflows.")

    updated_workflow = await WorkflowService.update_workflow_with_steps(workflow_id, workflow_data, steps_data)
    if updated_workflow:
        return updated_workflow
    raise HTTPException(status_code=404, detail="Workflow not found")

# @router.put("/update/{workflow_id}")
# async def update_workflow_with_steps(
#     workflow_id: str,
#     workflow_data: WorkflowCreate,
#     steps_data: List[WorkflowStepCreate],
#     credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
# ):
#     '''Nangyare dito sa update is get the workflow, then ma uupdate tapos si step delete muna lahat then insert new one'''
#     token = JWTRepo.extract_token(credentials)
#     roles = token.get('role', [])
#     if "research professor" not in roles:
#         raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to update workflows.")

#     updated_workflow = await WorkflowService.update_workflow_with_steps(workflow_id, workflow_data, steps_data)
#     if updated_workflow:
#         return updated_workflow
#     raise HTTPException(status_code=404, detail="Workflow not found")


# ===================================END



@router.get("/created-workflow-by-user", response_model=List[WorkflowDetail])
async def read_workflow_made_by_user(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''Hindi ito magagamit ata.. pero ginawa ko lang sana para ma display yung mga ginawa na workflow na ginawa ng research prof talaga'''
    
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

@router.get("/list/all", response_model=List[WorkflowDetail])
async def read_workflow(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])

    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    workflow = await WorkflowService.get_workflow_all()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.get("/{workflow_id}", response_model=WorkflowDetail)
async def read_workflow_by_id(workflow_id: str = Path(..., title="The ID of the workflow")):
    workflow = await WorkflowService.get_workflow_by_id_with_steps(workflow_id)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow


@router.delete("/delete-workflow/{workflow_id}", response_model=dict)
async def delete_workflow(workflow_id: str = Path(..., title="The ID of the workflow")):
    deleted = await WorkflowService.delete_workflow_by_id(workflow_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return {"message": "Workflow deleted successfully"}

# IBABABAALIK ko pag need
@router.delete("/delete-workflows-step/{workflow_step_id}", response_model=dict)
async def delete_workflow(workflow_step_id: str = Path(..., title="The ID of the workflow step")):
    deleted = await WorkflowService.delete_workflowstep_by_id(workflow_step_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Workflow step not found")

    return {"message": "Workflow deleted successfully"}


