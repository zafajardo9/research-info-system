from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.service.users_service import UserService
from app.model.student import Student  
from app.model.faculty import Faculty  

router = APIRouter(
    prefix="/users",
    tags=['user'],
    dependencies=[Depends(JWTBearer())]
)

@router.get("/profile/student", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_student_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    username = token['username']
    result = await UserService.get_student_profile(username)
    if result:
        return ResponseSchema(detail="Successfully fetch student profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")

@router.get("/profile/faculty", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_faculty_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    username = token['username']
    result = await UserService.get_faculty_profile(username)
    if result:
        return ResponseSchema(detail="Successfully fetch faculty profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Faculty profile not found")


@router.get("/student_list", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_student_list():
    """
    Get all student
    """
    result = await UserService.get_all_student()
    if result:
        return ResponseSchema(detail="Successfully fetch Student profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")


@router.get("/faculty_list", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_faculty_list():
    """
    Get all faculty member
    """

    result = await UserService.get_all_faculty()
    if result:
        return ResponseSchema(detail="Successfully fetch faculty profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
