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

# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    async def register_student(register: RegisterSchema):
        # Create uuid
        _student_id = str(uuid4())
        _users_id = str(uuid4())
        birth_date = datetime.strptime(register.birth, '%d-%m-%Y')

        _section = await SectionService.find_section_course(register.section,register.course)

        # Mapping request data to class entity table
        _student = Student(
                        id=_student_id,
                        name=register.name,
                        birth=birth_date,
                        year=register.year,
                        student_number=register.student_number,
                        phone_number=register.phone_number,
                        class_id=_section.id
                        )
        _role = await RoleRepository.find_by_role_name("student")
        
        _users_role = UsersRole(users_id=_users_id, role_id=_role.id)
        _users = Users(
                        id=_users_id,
                        username=register.username,
                        email=register.email,
                        password=pwd_context.hash(register.password),
                        student_id=_student_id,
                        student_number=register.student_number, 
                        )

        await StudentRepository.create(db, **_student.dict())
        await UsersRepository.create(db, **_users.dict())
        await UserRoleRepository.create(db, **_users_role.dict())
        

    @staticmethod
    async def register_faculty(register: RegisterSchemaFaculty):
        # Create uuid
        _faculty_id = str(uuid4())
        _users_id = str(uuid4())
        birth_date = datetime.strptime(register.birth, '%d-%m-%Y')

        # Mapping request data to class entity table
        _faculty = Faculty(
            id=_faculty_id,
            name=register.username,
            birth=birth_date,
            phone_number=register.phone_number,
        )
        _role = await RoleRepository.find_by_role_name("faculty")
        _users_role = UsersRole(users_id=_users_id, role_id=_role.id)
        _users = Users(
            id=_users_id,
            username=register.username,
            email=register.email,
            password=pwd_context.hash(register.password),
            faculty_id=_faculty_id,
        )


        # Insert to tables
        await FacultyRepository.create(db, **_faculty.dict())
        await UsersRepository.create(db, **_users.dict())
        await UserRoleRepository.create(db, **_users_role.dict())

    # ===============================
    @staticmethod
    async def login_student(login: LoginSchema):
        # Check the Users table for a username match
        _user_by_username = await UsersRepository.find_by_username(login.username)

        if _user_by_username is not None:
            # Check if the user has the "student" role
            user_roles = await UsersRepository.get_user_roles(_user_by_username.id)

            if "student" not in user_roles:
                raise HTTPException(status_code=403, detail="Access forbidden. Only students are allowed.")

            # Check the password
            if not pwd_context.verify(login.password, _user_by_username.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            # Generate and return the JWT token
            return JWTRepo(data={"username": _user_by_username.username, "user_id": _user_by_username.id, "role": user_roles}).generate_token()

        # Check the Users table for a student number match
        _user_by_student_number = await UsersRepository.find_by_student_number(login.username)

        if _user_by_student_number is not None:
            # Check if the user has the "student" role
            user_roles = await UsersRepository.get_user_roles(_user_by_student_number.id)

            if "student" not in user_roles:
                raise HTTPException(status_code=403, detail="Access forbidden. Only students are allowed.")

            # Check the password
            if not pwd_context.verify(login.password, _user_by_student_number.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            # Generate and return the JWT token
            return JWTRepo(data={"username": _user_by_student_number.username, "user_id": _user_by_student_number.id, "role": user_roles}).generate_token()

        raise HTTPException(status_code=404, detail="Student not found or invalid role!")



    #  NEED BALIKAN DAPAT KASI PWEDE EMAIL
    @staticmethod
    async def login_faculty(login: LoginSchema):
        # Check the Users table for a username match
        _user_by_username = await UsersRepository.find_by_username(login.username)

        if _user_by_username is not None:
            # Check if the user has the "faculty" role
            user_roles = await UsersRepository.get_user_roles(_user_by_username.id)

            if "faculty" not in user_roles:
                raise HTTPException(status_code=403, detail="Access forbidden. Only faculty members are allowed.")

            # Check the password
            if not pwd_context.verify(login.password, _user_by_username.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            # Generate and return the JWT token
            return JWTRepo(data={"username": _user_by_username.username, "user_id": _user_by_username.id, "role": user_roles}).generate_token()

        # Check the Users table for a student number match
        _user_by_email = await UsersRepository.find_by_email(login.username)

        if _user_by_email is not None:
            # Check if the user has the "student" role
            user_roles = await UsersRepository.get_user_roles(_user_by_email.id)

            if "faculty" not in user_roles:
                raise HTTPException(status_code=403, detail="Access forbidden. Only faculty are allowed.")

            # Check the password
            if not pwd_context.verify(login.password, _user_by_email.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            # Generate and return the JWT token
            return JWTRepo(data={"username": _user_by_email.username, "user_id": _user_by_email.id, "role": user_roles}).generate_token()

        raise HTTPException(status_code=404, detail="Faculty not found or invalid role!")

    #  NEED BALIKAN DAPAT KASI PWEDE EMAIL
    @staticmethod
    async def login_admin(login: LoginSchema):
        # Check the Users table for a username match
        _user_by_username = await UsersRepository.find_by_username(login.username)

        if _user_by_username is not None:
            # Check if the user has the "faculty" role
            user_roles = await UsersRepository.get_user_roles(_user_by_username.id)

            if "admin" not in user_roles:
                raise HTTPException(status_code=403, detail="Access forbidden. Only admin are allowed.")

            # Check the password
            if not pwd_context.verify(login.password, _user_by_username.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            # Generate and return the JWT token
            return JWTRepo(data={"username": _user_by_username.username, "user_id": _user_by_username.id, "role": user_roles}).generate_token()

        # Check the Users table for a student number match
        _user_by_email = await UsersRepository.find_by_email(login.username)

        if _user_by_email is not None:
            # Check if the user has the "student" role
            user_roles = await UsersRepository.get_user_roles(_user_by_email.id)

            if "admin" not in user_roles:
                raise HTTPException(status_code=403, detail="Access forbidden. Only admin are allowed.")

            # Check the password
            if not pwd_context.verify(login.password, _user_by_email.password):
                raise HTTPException(status_code=400, detail="Invalid Password!")

            # Generate and return the JWT token
            return JWTRepo(data={"username": _user_by_email.username, "user_id": _user_by_email.id, "role": user_roles}).generate_token()

        raise HTTPException(status_code=404, detail="Faculty not found or invalid role!")

    


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