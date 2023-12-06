from typing import List
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.service.users_service import UserService
from app.model.student import Student  
from app.model.faculty import Faculty
from app.repository.users import UsersRepository
from app.model.workflowprocess import Course

router = APIRouter(
    prefix="/users",
    tags=['user'],
    dependencies=[Depends(JWTBearer())]
)

@router.get("/profile/student", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_student_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    username = token['username']
    roles = token.get('role', [])

    if "student" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only students are allowed.")

    result = await UserService.get_student_profile(username)
    if result:
        return ResponseSchema(detail="Successfully fetch student profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")

@router.get("/profile/faculty", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_faculty_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    username = token['username']
    user_id = token['user_id']
    roles = await UsersRepository.get_user_roles(user_id)
    result = await UserService.get_faculty_profile(username)

    if "faculty" not in roles and "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only faculty members are allowed.")
    
    if result:
        result_dict = dict(result)
        result_dict['roles'] = roles
        return ResponseSchema(detail="Successfully fetch faculty profile!", result=result_dict)
    else:
        raise HTTPException(status_code=404, detail="Faculty profile not found")

@router.get("/profile/student/{user_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_student_profile_by_ID(user_id: str):

    roles = await UsersRepository.get_user_roles(user_id)
    result = await UserService.get_student_profile_by_ID(user_id)
    
    if result:
        result_dict = dict(result)
        result_dict['roles'] = roles
        return ResponseSchema(detail="Successfully fetch student profile by ID!", result=result_dict)
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")


@router.get("/profile/faculty/{user_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_faculty_profile_by_ID(user_id: str):

    roles = await UsersRepository.get_user_roles(user_id)
    result = await UserService.get_faculty_profile_by_ID(user_id)
    
    if result:
        result_dict = dict(result)
        result_dict['roles'] = roles
        return ResponseSchema(detail="Successfully fetch faculty profile by ID!", result=result_dict)
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
        raise HTTPException(status_code=404, detail="Faculty list not found")

@router.get("/research_prof_list", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_prof_list():
    """
    Get all faculty member
    """

    result = await UserService.get_all_research_prof()
    if result:
        return ResponseSchema(detail="Successfully fetch faculty profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Research Profesor list not found")
    

@router.get("/admin_list", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_admin_list():
    """
    Get all faculty member
    """

    result = await UserService.get_all_admin()
    if result:
        return ResponseSchema(detail="Successfully fetch faculty profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Admin list not found")
    

@router.get("/users_faculty_with_roles", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_users_with_roles():
    """
    Get all users with their roles
    """

    result = await UserService.get_all_in_faculty_with_roles()
    
    if result:
        formatted_result = UserService.format_users_with_roles(result)
        return ResponseSchema(detail="Successfully fetched user profiles with roles!", result=formatted_result)
    else:
        raise HTTPException(status_code=404, detail="User list not found")


@router.get("/all_user", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_list():
    """
    Get all user in USER TABLE
    """
    result = await UserService.get_all_list()
    if result:
        return ResponseSchema(detail="Successfully fetch all users!", result=result)
    else:
        raise HTTPException(status_code=404, detail="User profile not found")


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




@router.get("/course_list")
async def get_courses():
    """
    Get all courses with their descriptions
    """
    return course_descriptions


@router.get("/course_with_year_list")
async def get_courses():
    """
    Mga nasa Table lang for now
    """
    
    result = await UsersRepository.filter_student_year_course()
    if result:
        return ResponseSchema(detail="Successfully fetch all year and course!", result=result)
    else:
        raise HTTPException(status_code=404, detail="No data found")


# todo for putting research adviser to a particular ang section