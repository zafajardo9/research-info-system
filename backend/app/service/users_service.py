from sqlalchemy import func, or_, outerjoin, select, and_
from app.model import Role, Users, UsersRole, Class
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
                Student.student_number,
                Student.phone_number,
                Class.section,
                Class.course
            )
            .join(Student, Users.student_id == Student.id)
            .join(Class, Student.class_id == Class.id)
            .where(Users.username == username)
        )
        return (await db.execute(query)).mappings().one_or_none()
    
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
    async def get_student_profile_by_ID(user_id: str):
        query = (
            select(
                Users.id,
                Users.username,
                Users.email,
                Student.name,
                Student.birth,
                Student.year,
                Student.student_number,
                Student.phone_number,
                Class.section,
                Class.course
            )
            .join(Student, Users.student_id == Student.id)
            .join(Class, Student.class_id == Class.id)
            .where(Users.id == user_id)
        )
        return (await db.execute(query)).mappings().one()
    
    
    @staticmethod
    async def get_faculty_profile_by_ID(user_id: str):
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
            .where(Users.id == user_id)
        )
        return (await db.execute(query)).mappings().one()

    @staticmethod
    async def getprofile(user_id: str):
        query = (
            select(
                Users.id,
                Users.username,
                Users.email,
                Faculty.name
            )
            .join_from(Users, Faculty)
            .where(Users.id == user_id)
        )
        return (await db.execute(query)).mappings().first()
#asdfasdfadf

    @staticmethod
    async def get_all_student():
        query = (
            select(
                Users.id,
                Users.username,
                Users.email,
                Student.name,
                Student.birth,
                Student.year,
                Student.student_number,
                Student.phone_number,
                Class.section,
                Class.course
            )
            .join(Student, Users.student_id == Student.id)
            .join(Class, Student.class_id == Class.id)
            .where(Role.role_name == "student")
        )

        result = await db.execute(query)
        students_data = result.mappings().all()

        return students_data
    
    

    @staticmethod
    async def get_all_faculty():
        query = (
            select(Users.id, Users.username, Users.email, Users.faculty_id, Faculty.name)
            .select_from(
                outerjoin(Users, Faculty).join(UsersRole).join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                or_(
                    Role.role_name == "faculty",
                    Role.role_name == "research professor",
                    Role.role_name == "research adviser",
                    Role.role_name == "admin",
                ),
                ))
            )
        )

        result = await db.execute(query)
        faculty_data = result.mappings().all()

        return faculty_data
    
    @staticmethod
    async def get_all_research_adviser():
        query = (
            select(Users.id, Users.username, Users.email, Users.faculty_id, Faculty.name)
            .select_from(
                outerjoin(Users, Faculty).join(UsersRole).join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                    Role.role_name == "research adviser",
                ))
            )
        )

        result = await db.execute(query)
        faculty_data = result.mappings().all()

        return faculty_data

    @staticmethod
    async def get_all_research_prof():
        query = (
            select(Users.id, Users.username, Users.email, Users.faculty_id, Faculty.name)
            .select_from(
                outerjoin(Users, Faculty).join(UsersRole).join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                    Role.role_name == "research professor",
                ))
            )
        )

        result = await db.execute(query)
        research_prof_data = result.mappings().all()

        return research_prof_data
    
    @staticmethod
    async def get_all_admin():
        query = (
            select(Users.id, Users.username, Users.email, Users.faculty_id, Faculty.name)
            .select_from(
                outerjoin(Users, Faculty).join(UsersRole).join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                    Role.role_name == "admin",
                ))
            )
        )

        result = await db.execute(query)
        admin_data = result.mappings().all()

        return admin_data


    @staticmethod
    async def get_all_list():
        query = (
            select(Users)
        )

        result = await db.execute(query)
        all_user = result.scalars().all()

        return all_user
    

    @staticmethod
    async def get_all_in_faculty_with_roles():
        query = (
            select(
                Users.id,
                Users.username,
                Users.email,
                Users.faculty_id,
                Faculty.name.label("faculty_name"),
                Role.role_name
            )
            .select_from(
                outerjoin(Users, Faculty)
                .join(UsersRole)
                .join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                ))
            )
            .where(or_(
                Role.role_name == "faculty",
                Role.role_name == "admin",
                Role.role_name == "research professor",
                Role.role_name == "research adviser",
            ))
        )

        result = await db.execute(query)
        faculty_data = result.mappings().all()

        return faculty_data

    @staticmethod
    def format_users_with_roles(users_with_roles):
        formatted_result = {}
        
        for user_role in users_with_roles:
            user_id = user_role["id"]
            
            if user_id not in formatted_result:
                # Initialize user entry if not exists
                formatted_result[user_id] = {
                    "id": user_role["id"],
                    "username": user_role["username"],
                    "email": user_role["email"],
                    # "faculty_id": user_role["faculty_id"],
                    "faculty_name": user_role["faculty_name"],
                    "role_names": [user_role["role_name"]],
                }
            else:
                # Add role to existing user entry
                formatted_result[user_id]["role_names"].append(user_role["role_name"])

        return list(formatted_result.values())