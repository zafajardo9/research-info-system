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
from app.repository.users import UsersRepository
from app.schema import LoginSchema, ForgotPasswordSchema
from app.repository.auth_repo import JWTRepo
from app.model.users import Users

from app.config import db

# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    async def register_student(register: RegisterSchema):
        # Create uuid
        _student_id = str(uuid4())
        _users_id = str(uuid4())

        # Convert birth date type from frontend str to date
        birth_date = datetime.strptime(register.birth, '%d-%m-%Y')


        # Mapping request data to class entity table
        _student = Student(
                        id=_student_id,
                        name=register.name,
                        birth=birth_date,
                        year=register.year, 
                        section=register.section,  
                        course=register.course, 
                        student_number=register.student_number,
                        phone_number=register.phone_number,
                        )
        _users = Users(
                        id=_users_id,
                        username=register.username,
                        email=register.email,
                        password=pwd_context.hash(register.password),
                        student_id=_student_id,
                        roles="student",
                        student_number=register.student_number, 
                        )
        await StudentRepository.create(db, **_student.dict())
        await UsersRepository.create(db, **_users.dict())

    @staticmethod
    async def register_faculty(register: RegisterSchemaFaculty):
        # Create uuid
        _faculty_id = str(uuid4())
        _users_id = str(uuid4())

        # Convert birth date type from frontend str to date
        birth_date = datetime.strptime(register.birth, '%d-%m-%Y')

        # Mapping request data to class entity table
        _faculty = Faculty(
            id=_faculty_id,
            name=register.username,
            birth=birth_date,
            phone_number=register.phone_number,
        )

        _users = Users(
            id=_users_id,
            username=register.username,
            email=register.email,
            password=pwd_context.hash(register.password),
            faculty_id=_faculty_id,
            roles="faculty",
        )


        # Insert to tables
        await FacultyRepository.create(db, **_faculty.dict())
        await UsersRepository.create(db, **_users.dict())

    # ===============================
    @staticmethod
    async def login_student(login: LoginSchema):
        # Check the Users table for a username match

        _user_by_username = await UsersRepository.find_by_username(login.username)
        
        # USERNAME
        if _user_by_username is not None and _user_by_username.roles == "student":
            if not pwd_context.verify(login.password, _user_by_username.password):
                raise HTTPException(
                    status_code=400, detail="Invalid Password !")
            return JWTRepo(data={"username": _user_by_username.username, "user_id": _user_by_username.id, "role": _user_by_username.roles}).generate_token()

        # STUDENT NUMBER
        _user_by_student_number = await UsersRepository.find_by_student_number(login.username)
        if _user_by_student_number is not None and _user_by_student_number.roles == "student":
            if not pwd_context.verify(login.password, _user_by_student_number.password):
                raise HTTPException(
                    status_code=400, detail="Invalid Password !")
            return JWTRepo(data={"username": _user_by_student_number.username, "user_id": _user_by_username.id}).generate_token()

        raise HTTPException(status_code=404, detail="Student not found or invalid role!")



#NEED BALIKAN DAPAT KASI PWEDE EMAIL
    @staticmethod
    async def login_faculty(login: LoginSchema):
        _user = await UsersRepository.find_by_username(login.username)

        if _user is not None and _user.roles == "faculty":
            if not pwd_context.verify(login.password, _user.password):
                raise HTTPException(
                    status_code=400, detail="Invalid Password !")
            return JWTRepo(data={"username": _user.username, "user_id": _user.id, "role": _user.roles}).generate_token()

        raise HTTPException(status_code=404, detail="Faculty not found or invalid role!")