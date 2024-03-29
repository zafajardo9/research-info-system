from typing import List, Optional
from sqlalchemy import and_, select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from app.config import db
from app.model.users import Role, Users, UsersRole
from app.repository.base_repo import BaseRepo
from app.model.student import Student
from app.model.faculty import Faculty


class UsersRepository(BaseRepo):
    model = Users

    
    @staticmethod
    async def get_user_roles(user_id: str) -> List[str]:
        query = (
            select(Role.role_name)
            .join(UsersRole, Role.id == UsersRole.role_id)
            
            .where(UsersRole.users_id == user_id)
        )

        roles = (await db.execute(query)).scalars().all()
        return roles

    #Student Login
    @staticmethod
    async def find_by_student_number(student_number: str):
        query = select(Student).where(Student.StudentNumber == student_number)
        return (await db.execute(query)).scalar_one_or_none()
    
    
    #get id
    @staticmethod
    async def get_student_user_table_id(student_id: int):
        query = select(Users).where(Users.student_id == student_id)
        return (await db.execute(query)).scalar_one_or_none()
    
    @staticmethod
    async def get_faculty_user_table_id(faculty_id: int):
        query = select(Users).where(Users.faculty_id == faculty_id)
        return (await db.execute(query)).scalar_one_or_none()
    
    #checkers
    @staticmethod
    async def checker_find_student_in_user_table(student_id: int) -> bool:
        query = select(Users).where(Users.student_id == student_id)
        user_in_users_table = (await db.execute(query)).scalar_one_or_none()
        return user_in_users_table is not None
    
    @staticmethod
    async def checker_find_faculty_in_user_table(faculty_id: int) -> bool:
        query = select(Users).where(Users.faculty_id == faculty_id)
        user_in_users_table = (await db.execute(query)).scalar_one_or_none()
        return user_in_users_table is not None
    # CHECKER END============================
    
    @staticmethod
    async def find_by_user_id(user_id: str):
        query = select(Users).where(Users.id == user_id)
        return (await db.execute(query)).scalar_one_or_none()

    #Faculty Login
    @staticmethod
    async def find_by_email(email: str):
        query = select(Faculty).where(Faculty.Email == email)
        return (await db.execute(query)).scalar_one_or_none()
    


    
    @staticmethod
    async def fetch_student_by_user_id(user_id: str):
        query = select(
            Users.id,
            Student.id,
            Student.Email,
            Student.Password,
            ).where(Users.id == user_id)
        return (await db.execute(query)).fetchall()
    # @staticmethod
    # async def find_by_email_faculty(email: str):
    #     query = select(Faculty).where(Faculty.Email == email)
    #     return (await db.execute(query)).scalar_one_or_none()
    
    # @staticmethod
    # async def find_by_email_student(email: str):
    #     query = select(Student).where(Student.Email == email)
    #     return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update_password(user: Users, password: str):
        user.password = password
        await db.commit()
        

    
    
    @staticmethod
    async def assign_role(user_id: int, role: str):
        role = await db.execute(select(Role).where(Role.role_name == role))
        role = role.scalar_one_or_none()
        if role:
            user_role = UsersRole(users_id=user_id, role_id=role.id)
            db.add(user_role)

        await db.commit()

    @staticmethod
    async def filter_student_year_course():
        query = select(Student.course, Student.section).distinct()
        return (await db.execute(query)).fetchall()
    
    
    #ROLE CHECKER
    @staticmethod
    async def has_role(user_id: str, target_role: str) -> bool:
        """
        Check if a user has a specific role.

        Args:
            session (AsyncSession): SQLAlchemy async session.
            user_id (str): ID of the user.
            target_role (str): Target role to check.

        Returns:
            bool: True if the user has the specified role, False otherwise.
        """
        # Query the role ID based on the role name
        role = await db.execute(select(Role).where(Role.role_name == target_role))
        role = role.scalar_one_or_none()

        if role:
            # Check if the user has the specified role
            user_role = await db.execute(
                select(UsersRole)
                .where((UsersRole.users_id == user_id) & (UsersRole.role_id == role.id))
            )
            return user_role.scalar_one_or_none() is not None

        return False
    
    @staticmethod
    async def remove_role(user_id: int, role: str):
        # Find the role
        role = await db.execute(select(Role).where(Role.role_name == role))
        role = role.scalar_one_or_none()
        if role:
            # Find the user role
            user_role = await db.execute(select(UsersRole).where((UsersRole.users_id == user_id) & (UsersRole.role_id == role.id)))
            user_role = user_role.scalar_one_or_none()

            # If the user has this role, remove it
            if user_role:
                await db.execute(UsersRole.__table__.delete().where((UsersRole.users_id == user_id) & (UsersRole.role_id == role.id)))

        await db.commit()