from operator import itemgetter
from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, NavigationTabCreate, ResponseSchema, UpdateAssign, UpdateResearchTypeAssign, UpdateWorkflowData, UpdateWorkflowsByType, UserWithAssignments, WorkflowCreate, WorkflowCreateWithSteps, WorkflowDetail, WorkflowGroupbyType, WorkflowStepCreate, WorkflowStepDetail
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



@router.post("/create", response_model=List[Workflow])
async def create_workflows2(workflow_data: WorkflowCreate, workflow_steps: List[WorkflowStepCreate], credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    created_workflows = []
    for class_id in workflow_data.class_id:
        if await WorkflowService.check_if_workflow_exists(workflow_data.type, class_id):
            continue
        
        created_workflow = await WorkflowService.create_workflow(workflow_data.type, class_id, current_user)

        for increment, step_data in enumerate(workflow_steps, start=1):
            created_workflow_step = await WorkflowService.create_workflow_step(step_data, increment, created_workflow.id)

        created_workflows.append(created_workflow)

    return created_workflows
#==========================UPDATE

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

@router.put("/update", response_model=List[Workflow])
async def update_workflows(update_data: UpdateWorkflowData, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])
    
    # Check if the user has the necessary role to update workflows
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to update workflows.")

    updated_workflows = []
    
    for workflow_id in update_data.workflow_id:
        db_workflow = await WorkflowService.get_workflow_by_id(workflow_id)
        
        if db_workflow:
            # Clear existing steps and add new steps
            await WorkflowService.clear_workflow_steps(workflow_id)
            
            for increment, step_data in enumerate(update_data.steps_data, start=1):
                created_workflow_step = await WorkflowService.create_workflow_step(step_data, increment, workflow_id)

            updated_workflows.append(db_workflow)
    
    return updated_workflows

@router.put("/update_by_type", response_model=List[Workflow])
async def update_workflows_by_type(update_data: UpdateWorkflowsByType, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])
    
    # Check if the user has the necessary role to update workflows
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to update workflows.")

    updated_workflows = []
    
    # Query workflows by type
    workflows = await WorkflowService.get_workflows_by_type(update_data.research_type)
    
    for workflow in workflows:
        # Clear existing steps and add new steps
        await WorkflowService.clear_workflow_steps(workflow.id)
        
        for increment, step_data in enumerate(update_data.steps_data, start=1):
            created_workflow_step = await WorkflowService.create_workflow_step(step_data, increment, workflow.id)

        updated_workflows.append(workflow)
    
    return updated_workflows


# ===================================END


# todo FIX THIS to show section and course
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
    roles = token.get('role', [])

    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    workflow = await WorkflowService.get_workflow_all()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="No Workflow Found")
    return workflow

@router.get("/{type}", response_model=List[WorkflowDetail])
async def read_workflow(type: str, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])

    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    workflow = await WorkflowService.get_workflow_all_by_type(type)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="No Workflow Found")
    return workflow

@router.get("/workflow-info/{workflow_id}", response_model=WorkflowDetail)
async def read_workflow_by_id(workflow_id: str = Path(..., title="The ID of the workflow")):
    workflow_query = await WorkflowService.get_workflow_by_id_with_steps(workflow_id)
    
    if not workflow_query:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow_query


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


