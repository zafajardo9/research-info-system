from operator import itemgetter
from typing import Dict, List
import uuid
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import WorkflowCreate, WorkflowCreateWithSteps, WorkflowDetail, WorkflowGroupbyType, WorkflowResponse, WorkflowStepCreate, WorkflowStepDetail, WorkflowUpdate
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

from sqlalchemy.orm import selectinload
from app.config import db
from app.model.faculty import Faculty
from app.model.workflowprocess import NavigationTab, WorkflowClass
from app.model.student import Class

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
async def create_workflows(workflow_data: WorkflowCreate, workflow_steps: List[WorkflowStepCreate], credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])
    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    # Create workflow
    created_workflow = await WorkflowService.create_workflow(workflow_data.type, current_user)

    # Create steps
    for step_data in workflow_steps:
        await WorkflowService.create_workflow_step(step_data, created_workflow.id)

    # Associate workflow with classes
    for class_id in workflow_data.class_id:
        await WorkflowService.create_workflow_class_association(created_workflow.id, class_id)

    return [created_workflow]
#==========================UPDATE

@router.post("/create-step/{workflow_id}", response_model=List[WorkflowStepCreate])
async def update_workflow(
    workflow_id: str,
    workflow_steps: List[WorkflowStepCreate],
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):
    token = JWTRepo.extract_token(credentials)
    
    created_workflow_steps = []

    for step_data in workflow_steps:
        created_step = await WorkflowService.create_workflow_step(step_data, workflow_id)
        created_workflow_steps.append(created_step)

    return created_workflow_steps


@router.post("/add_class/{workflow_id}", response_model=List[WorkflowClass])
async def add_class(
    workflow_id: str,
    workflow_data: List[str]
):
    created = []
    for class_id in workflow_data:
        created_class = await WorkflowService.create_workflow_class_association(workflow_id, class_id)
        created.append(created_class)


    return created





# @router.put("/update/{workflow_id}", response_model=List[Workflow])
# async def update_workflow(
#     workflow_id: str,
#     updated_data: WorkflowUpdate,
#     updated_steps: List[WorkflowStepCreate],
#     credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
# ):
#     try:
#         # Check if the workflow exists
#         workflow = await db.get(Workflow, workflow_id)
#         if not workflow:
#             raise HTTPException(status_code=404, detail="Workflow not found")

#         # Update workflow data
#         for key, value in updated_data.dict().items():
#             setattr(workflow, key, value)

#         # Fetch existing steps
#         existing_steps = await db.execute(
#             select(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id)
#         )
#         existing_steps = existing_steps.scalars().all()

#         # Update existing steps and add new steps
#         updated_steps_mapping = {step.name: step for step in updated_steps}
#         for existing_step in existing_steps:
#             if existing_step.name in updated_steps_mapping:
#                 # Update existing step
#                 updated_step_data = updated_steps_mapping[existing_step.name]
#                 for key, value in updated_step_data.dict().items():
#                     setattr(existing_step, key, value)
#                 # Remove updated step from the mapping to handle new steps later
#                 del updated_steps_mapping[existing_step.name]

#         # Add new steps
#         new_steps = [
#             WorkflowStep(
#                 id=str(uuid.uuid4()),
#                 workflow_id=workflow_id,
#                 **step.dict()
#             ) for step in updated_steps_mapping.values()
#         ]
#         db.add_all(new_steps)

#         await db.commit()

#         # Fetch the updated workflow
#         updated_workflow = await db.get(Workflow, workflow_id)

#         return [updated_workflow]

#     except Exception as e:
#         # Rollback in case of any error
#         await db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))





@router.put("/update-steps/{workflow_id}", response_model=List[WorkflowStep])
async def update_workflow_steps(
    workflow_id: str,
    updated_steps: List[WorkflowStepCreate]
):
    try:
        # Check if the workflow exists
        workflow = await db.get(Workflow, workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Fetch the existing steps
        existing_steps = await db.execute(
            select(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id)
        )
        existing_steps = existing_steps.scalars().all()

        # Update existing steps and add new steps
        updated_steps_mapping = {step.name: step for step in updated_steps}
        for existing_step in existing_steps:
            if existing_step.name in updated_steps_mapping:
                # Update existing step
                updated_step_data = updated_steps_mapping[existing_step.name]
                for key, value in updated_step_data.dict().items():
                    setattr(existing_step, key, value)
                # Remove updated step from the mapping to handle new steps later
                del updated_steps_mapping[existing_step.name]

        # Add new steps
        new_steps = [
            WorkflowStep(
                id=str(uuid.uuid4()),
                workflow_id=workflow_id,
                **step.dict()
            ) for step in updated_steps_mapping.values()
        ]
        db.add_all(new_steps)

        await db.commit()

        # Fetch the updated steps
        updated_steps = await db.execute(
            select(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id)
        )
        updated_steps = updated_steps.scalars().all()

        return updated_steps

    except Exception as e:
        # Rollback in case of any error
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))





@router.put("/update/{workflow_id}/{step_id}", response_model=WorkflowStep)
async def update_workflow(
    workflow_id: str,
    step_id:str,
    workflow_data: WorkflowStepCreate
    ):
    try:
        # Check if the workflow exists
        workflow = await db.get(Workflow, workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        # Check if the step exists in the workflow
        step = await db.get(WorkflowStep, step_id)
        if not step or step.workflow_id != workflow_id:
            raise HTTPException(status_code=404, detail="Step not found in the specified workflow")

        # Update the workflow attributes
        for key, value in workflow_data.dict().items():
            setattr(step, key, value)

        await db.commit()
        await db.refresh(step)

        return step

    except Exception as e:
        # Rollback in case of any error
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))




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


@router.get("/list/all", response_model=List[Dict])
async def get_all_workflows():
    workflows = await WorkflowService.get_workflow_all()
    return workflows



@router.get("/{type}", response_model=List[Dict])
async def read_workflow(type: str, credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])

    if "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    workflow = await WorkflowService.get_workflow_all_by_type(type)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="No Workflow Found")
    return workflow

@router.get("/workflow-info/{workflow_id}")
async def read_workflow_by_id(workflow_id: str = Path(..., title="The ID of the workflow")):
    workflow_query = await WorkflowService.get_workflow_all_by_id(workflow_id)
    
    if not workflow_query:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow_query


@router.delete("/delete-workflow/{workflow_id}", response_model=dict)
async def delete_workflow(workflow_id: str = Path(..., title="The ID of the workflow")):
    deleted = await WorkflowService.delete_workflow_by_id(workflow_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return {"message": "Workflow deleted successfully"}

@router.delete("/remove-class/{id}", response_model=dict)
async def remove_class(id: str):
    deleted = await WorkflowService.delete_class_id(id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Error")

    return {"message": "Successfully removed"}

# IBABABAALIK ko pag need
@router.delete("/delete-workflows-step/{workflow_step_id}", response_model=dict)
async def delete_workflow(workflow_step_id: str = Path(..., title="The ID of the workflow step")):
    deleted = await WorkflowService.delete_workflowstep_by_id(workflow_step_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Workflow step not found")

    return {"message": "Workflow deleted successfully"}


