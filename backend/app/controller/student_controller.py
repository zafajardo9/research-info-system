from typing import List
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.repository.auth_repo import JWTBearer, JWTRepo


from app.schema import ResponseSchema, WorkflowAllDetails, WorkflowCreate, WorkflowDetail, WorkflowStepCreate, WorkflowStepDetail
from app.service.users_service import UserService
from app.model.student import Student  
from app.model.faculty import Faculty
from app.repository.users import UsersRepository
from app.service.workflow_service import WorkflowService
from app.service.assignTo_service import AssignToSection  

router = APIRouter(
    prefix="/student",
    tags=['Student'],
    dependencies=[Depends(JWTBearer())]
)


@router.get("/myflow", response_model=List[WorkflowDetail])
async def read_workflow(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    username = token['username']
    roles = token.get('role', [])

    if "student" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")


    result = await UserService.get_student_profile(username)

    user_course = result['course']
    user_section = result['section']

    workflow = await WorkflowService.get_my_workflow(user_course, user_section)
    
    print(workflow) # Add this line
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.get("/your-workflow-status", response_model=List[WorkflowDetail])
async def read_workflow(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    username = token['username']
    roles = token.get('role', [])

    if "student" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")


    result = await UserService.get_student_profile(username)

    user_course = result['course']
    user_section = result['section']

    workflow = await WorkflowService.get_my_workflow(user_course, user_section)
    

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.get("/my-adviser-list"  )
async def read_workflow(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    username = token['username']
    roles = token.get('role', [])

    if "student" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")


    result = await UserService.get_student_profile(username)

    user_course = result['course']
    user_section = result['section']

    advisers_assigned = await AssignToSection.student_get_adviser_list(user_course, user_section)
    
    print(advisers_assigned) # Add this line
    if not advisers_assigned:
        raise HTTPException(status_code=404, detail="Nothing found")
    return advisers_assigned


@router.get("/my-research-professor-list")
async def read_workflow(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    username = token['username']
    roles = token.get('role', [])

    if "student" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")


    result = await UserService.get_student_profile(username)

    user_course = result['course']
    user_section = result['section']

    advisers_assigned = await AssignToSection.student_get_prof_list(user_course, user_section)
    
    print(advisers_assigned) # Add this line
    if not advisers_assigned:
        raise HTTPException(status_code=404, detail="Nothing found")
    return advisers_assigned


# todo making a workflow that shows the status of the step it is connected


@router.get("/workflow/{workflow_id}")
async def get_workflow_details(workflow_id: str):
    workflow = await WorkflowService.get_my_workflow_by_id(workflow_id)
    #workflowstep_id = workflow['woq']
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow