import base64
from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from passlib.context import CryptContext
from app.schema import RegisterSchema, RegisterSchemaFaculty
from app.model.student import Student
from app.model.faculty import Faculty
from app.repository.student_repo import StudentRepository
from app.repository.faculty_repo import FacultyRepository
from app.repository.user_role_repo import UserRoleRepository
from app.repository.role_repo import RoleRepository
from app.repository.users import UsersRepository
from app.schema import LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTRepo
from app.model.users import Users, UsersRole, Role

from app.config import db
from app.service.section_service import SectionService
from sqlalchemy import select


from werkzeug.security import generate_password_hash, check_password_hash


class AuthService:
    @staticmethod
    async def put_student(student_id: int):
        _users_id = str(uuid4())
        _role = await RoleRepository.find_by_role_name("student")
        _users_role = UsersRole(users_id=_users_id, role_id=_role.id)
        _users = Users(
                        id=_users_id,
                        student_id=student_id,
                        )
        await UsersRepository.create(db, **_users.dict())
        await UserRoleRepository.create(db, **_users_role.dict())
    
    @staticmethod
    async def put_faculty(faculty_id: int):
        _users_id = str(uuid4())
        _role = await RoleRepository.find_by_role_name("faculty")
        _users_role = UsersRole(users_id=_users_id, role_id=_role.id)
        _users = Users(
                        id=_users_id,
                        faculty_id=faculty_id,
                        )
        await UsersRepository.create(db, **_users.dict())
        await UserRoleRepository.create(db, **_users_role.dict())


    # ===============================
    @staticmethod
    async def login_student(login: LoginSchema):

        _user_by_student_number = await UsersRepository.find_by_student_number(login.username)

        if _user_by_student_number is not None:
            

            # Check the password
            if not check_password_hash(_user_by_student_number.Password, login.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            #CHECK THEN CREATE IF WALA
            user_exists_in_users_table = await UsersRepository.checker_find_student_in_user_table(_user_by_student_number.StudentId)
            
            if not user_exists_in_users_table:
                await AuthService.put_student(_user_by_student_number.StudentId)
            
            user_id = await UsersRepository.get_student_user_table_id(_user_by_student_number.StudentId)
            user_roles = await UsersRepository.get_user_roles(user_id.id)
            
            # Generate and return the JWT token
            return JWTRepo(data={"user_id": user_id.id, "student_id": _user_by_student_number.StudentId, "role": user_roles}).generate_token()


        raise HTTPException(status_code=404, detail="Student not found or invalid role!")



    #  NEED BALIKAN DAPAT KASI PWEDE EMAIL
    @staticmethod
    async def login_faculty(login: LoginSchema):

        # Check the Users table for a student number match
        _user_by_email = await UsersRepository.find_by_email(login.username)

        if _user_by_email is not None:

            # Check the password
            if not check_password_hash(_user_by_email.Password, login.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            #CHECK THEN CREATE IF WALA
            user_exists_in_users_table = await UsersRepository.checker_find_faculty_in_user_table(_user_by_email.FacultyId)
            
            if not user_exists_in_users_table:
                await AuthService.put_faculty(_user_by_email.FacultyId)

            user_id = await UsersRepository.get_faculty_user_table_id(_user_by_email.FacultyId)
            user_roles = await UsersRepository.get_user_roles(user_id.id)
            if "faculty" in user_roles:
                # Generate and return the JWT token
                return JWTRepo(data={"user_id": user_id.id,"faculty_id": _user_by_email.FacultyId, "role": user_roles}).generate_token()

        raise HTTPException(status_code=404, detail="Faculty not found or invalid role!")

    #  NEED BALIKAN DAPAT KASI PWEDE EMAIL
    @staticmethod
    async def login_admin(login: LoginSchema):

        
        _user_by_email = await UsersRepository.find_by_email(login.username)

        if _user_by_email is not None:

            # Check the password
            if not check_password_hash(_user_by_email.Password, login.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            user_id = await UsersRepository.get_faculty_user_table_id(_user_by_email.FacultyId)
            user_roles = await UsersRepository.get_user_roles(user_id.id)
            if "admin" in user_roles:
                return JWTRepo(data={"user_id": user_id.id,"faculty_id": _user_by_email.FacultyId, "role": user_roles}).generate_token()

        raise HTTPException(status_code=404, detail="Faculty not found or invalid role!")
    
    @staticmethod
    async def integration_auth():
        return JWTRepo(data={"user": "test_user", "token_generate": "success", "connection_type": "for integration"}).generate_token()


    @staticmethod
    async def verify_password(plain_password, hashed_password):
        return check_password_hash(hashed_password, plain_password)

    @staticmethod     
    async def update_user_password(user_id: str, current_password: str, new_password: str):
        query = (
            select(Student)
            .join(Users, Student.StudentId == Users.student_id)
            .filter(Users.id == user_id)
        )
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not await AuthService.verify_password(current_password, user.Password):
            raise HTTPException(status_code=400, detail="You have input a wrong current password")

        # Password verification passed, update the password
        user.Password = generate_password_hash(new_password, method='pbkdf2')
        await db.commit()
        db.refresh(user)
        return user


    @staticmethod     
    async def update_faculty_password(user_id: str, current_password: str, new_password: str):
        query = (
            select(Faculty)
            .join(Users, Faculty.FacultyId == Users.faculty_id)
            .filter(Users.id == user_id)
        )
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not await AuthService.verify_password(current_password, user.Password):
            raise HTTPException(status_code=400, detail="You have input a wrong current password")

        # Password verification passed, update the password
        user.Password = generate_password_hash(new_password, method='pbkdf2')
        await db.commit()
        db.refresh(user)
        return user

# Generate roles manually
async def generate_role():
    _role = await RoleRepository.find_by_list_role_name(["admin", "student", "faculty", "research professor"])
    if not _role:
        await RoleRepository.create_list(
            [
                Role(id=str(uuid4()), role_name="admin"), 
                Role(id=str(uuid4()), role_name="student"),
                Role(id=str(uuid4()), role_name="faculty"),
                Role(id=str(uuid4()), role_name="research professor"),
                Role(id=str(uuid4()), role_name="research adviser")
            ])
        
