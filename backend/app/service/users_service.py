from sqlalchemy import select
from app.model.users import Users
from app.model.student import Student  # Import the Student model
from app.model.faculty import Faculty  # Import the Faculty model
from app.config import db

class UserService:

    @staticmethod
    async def get_student_profile(username: str):
        query = (
            select(
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
                Users.username,
                Users.email,
                Faculty.name,
                Faculty.birth,
                Faculty.sex,  # Add other Faculty fields here
                Faculty.phone_number
            )
            .join_from(Users, Faculty)
            .where(Users.username == username)
        )
        return (await db.execute(query)).mappings().one()

    # The rest of your methods remain the same
