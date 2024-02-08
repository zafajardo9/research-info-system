from typing import List
from app.service.auth_service import AuthService
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import ForgotPassword, ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.service.users_service import UserService
from app.model.student import Student  
from app.model.faculty import Faculty
from app.repository.users import UsersRepository
from app.service.research_service import ResearchService
#from app.model.workflowprocess import Course


#Email
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from werkzeug.security import check_password_hash, generate_password_hash
from app.main import conf

router = APIRouter(
    prefix="/users",
    tags=['user'],
    dependencies=[Depends(JWTBearer())]
)

@router.get("/profile/student", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_student_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    _id = token['user_id']
    roles = token.get('role', [])

    if "student" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only students are allowed.")

    result = await UserService.get_student_profile(_id)
    if result:
        return ResponseSchema(detail="Successfully fetch student profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")


@router.post("/student/reset-password")
async def forgot_password(
    email: ForgotPassword, 
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    
    token = JWTRepo.extract_token(credentials)
    user_id = token['user_id']
    
    result = await AuthService.update_user_password(user_id, email.current_password, email.new_password)
    
    message = MessageSchema(
        subject="Password Reset",
        recipients=[result.Email],
        body=f"""You have successfully reset your password 
        
        This is your new password:
        <b>{email.new_password}</>""",
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    
    return {"message": "Password reset successfully. We also sent your password to your email"}


    # @staticmethod
    # async def update_status(db: Session, research_paper_id: str, new_status: Status) -> ResearchPaper:
    #     # Fetch the research paper
    #     result = await db.execute(select(ResearchPaper).where(ResearchPaper.id == research_paper_id))
    #     research_paper = result.scalar_one_or_none()

    #     if research_paper:
    #         research_paper.status = new_status
    #         await db.commit()
    #         db.refresh(research_paper)
    #         return research_paper
    #     else:
    #         raise HTTPException(status_code=404, detail="Research paper not found")


@router.get("/profile/faculty", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_faculty_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    user_id = token['user_id']
    roles = await UsersRepository.get_user_roles(user_id)
    result = await UserService.get_faculty_profile(user_id)

    if "faculty" not in roles and "research professor" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only faculty members are allowed.")
    
    if result:
        result_dict = dict(result)
        result_dict['roles'] = roles
        return ResponseSchema(detail="Successfully fetch faculty profile!", result=result_dict)
    else:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
    
@router.post("/faculty/reset-password")
async def forgot_password(
    email: ForgotPassword, 
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    
    token = JWTRepo.extract_token(credentials)
    id = token['user_id']
    
    result = await AuthService.update_faculty_password(id, email.new_password)
    
    
    message = MessageSchema(
        subject="Password Reset",
        recipients=[result.Email],
        body=f"""You have successfully reset your password 
        
        This is your new password:
        <b>{email.new_password}</>""",
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    
    return {"message": "Password reset successfully. We also sent your password to your email"}   
    


@router.get("/profile/student/{user_id}")
async def get_student_profile_by_ID(user_id: str):
    try:
        # Fetch roles, student profile, and papers asynchronously
        roles = await UsersRepository.get_user_roles(user_id)
        result = await UserService.get_student_profile(user_id)
        papers = await ResearchService.user_profile_papers(user_id)

        # Check if the student profile exists
        if result:
            result_dict = dict(result)
            result_dict['roles'] = roles
            result_dict['papers'] = papers

            # Return the collected information as a JSON response
            return result_dict
        else:
            raise HTTPException(status_code=404, detail="Student profile not found")

    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return {"error": f"An error occurred: {str(e)}"}


@router.get("/profile/faculty/{user_id}")
async def get_faculty_profile_by_ID(user_id: str):
    try: 
        roles = await UsersRepository.get_user_roles(user_id)
        result = await UserService.get_faculty_profile_by_ID(user_id)
        papers = await ResearchService.user_profile_papers_faculty(user_id)

        # Check if the student profile exists
        if result:
            result_dict = dict(result)
            result_dict['roles'] = roles
            result_dict['papers'] = papers

            return result_dict
        
        else:
            raise HTTPException(status_code=404, detail="Faculty profile not found")
    except Exception as e:
        # Handle exceptions and return an appropriate error response
        return {"error": f"An error occurred: {str(e)}"}


@router.get("/student_list", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_student_list():
    """
    Get all student
    """
    result = await UserService.get_all_students()
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
    

@router.get("/research_adviser_list", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_faculty_list():
    """
    Get all research adviser member
    """

    result = await UserService.get_all_research_adviser()
    if result:
        return ResponseSchema(detail="Successfully fetch adviser profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Research Adviser list not found")
    
    

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


def get_courses():
    return ["BSIT", "BBTLEDHE", "BTLEDICT", "BSBAHRM", "BSBA-MM", "BSENTREP", "BPAPFM", "DOMTMOM"]


@router.get("/course_list",)
async def get_list_of_courses():
    """
    Get all user in USER TABLE
    """
    courses = get_courses()
    return {"courses": courses}





# todo for putting research adviser to a particular ang section