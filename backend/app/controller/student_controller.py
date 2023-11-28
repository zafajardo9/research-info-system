from typing import List
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.repository.auth_repo import JWTBearer, JWTRepo


from app.schema import ResponseSchema, WorkflowCreate, WorkflowDetail, WorkflowStepCreate, WorkflowStepDetail
from app.service.users_service import UserService
from app.model.student import Student  
from app.model.faculty import Faculty
from app.repository.users import UsersRepository
from app.service.workflow_service import WorkflowService  

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

