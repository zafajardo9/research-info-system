from sqlalchemy import outerjoin, select
from app.model.users import Users
from app.model.student import Student  # Import the Student model
from app.model.faculty import Faculty  # Import the Faculty model
from app.config import db

class UserService:

    @staticmethod
    async def get_student_profile(username: str):
        query = (
            select(
                Users.id,
                Users.username,
                Users.email,
                Student.name,
                Student.birth,
                Student.year,
                Student.section,
                Student.course,
                Student.student_number,
                Student.phone_number
            )
            .join_from(Users, Student)
            .where(Users.username == username)
        )
        return (await db.execute(query)).mappings().one()
    
    @staticmethod
    async def get_faculty_profile(username: str):
        query = (
            select(
                Users.id,
                Users.username,
                Users.email,
                Faculty.name,
                Faculty.birth,
                Faculty.phone_number
            )
            .join_from(Users, Faculty)
            .where(Users.username == username)
        )
        return (await db.execute(query)).mappings().one()

    @staticmethod
    async def get_all_student():
        query = (
            select(Users.id, Users.username, Users.email, Users.student_id ,Student.student_number, Student.name, Student.section, Student.course)
            .select_from(outerjoin(Users, Student))
            .where(Users.roles == 'student')
        )

        result = await db.execute(query)
        students_data = result.mappings().all()

        return students_data
    

    @staticmethod
    async def get_all_faculty():
        query = (
            select(Users.id, Users.username, Users.email, Users.faculty_id, Faculty.name)
            .select_from(outerjoin(Users, Faculty))
            .where(Users.roles == 'faculty')
        )

        result = await db.execute(query)
        faculty_data = result.mappings().all()

        return faculty_data

    @staticmethod
    async def get_all_list():
        query = (
            select(Users)
        )

        result = await db.execute(query)
        all_user = result.scalars().all()

        return all_user
    