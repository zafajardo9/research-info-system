from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
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
    if token['role'] == "student":
        result = await UserService.get_student_profile(token['username'])
        return ResponseSchema(detail="Successfully fetch student profile!", result=result)
    else:
        return ResponseSchema(detail="Access denied for this profile", result=None)

@router.get("/profile/faculty", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_faculty_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    if token['role'] == "faculty":
        result = await UserService.get_faculty_profile(token['username'])
        return ResponseSchema(detail="Successfully fetch faculty profile!", result=result)
    else:
        return ResponseSchema(detail="Access denied for this profile", result=None)
