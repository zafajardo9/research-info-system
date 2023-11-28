from typing import List, Optional
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from app.config import db
from app.model.users import Role, Users, UsersRole
from app.repository.base_repo import BaseRepo


class UsersRepository(BaseRepo):
    model = Users

    @staticmethod
    async def find_by_username(username: str):
        query = select(Users).where(Users.username == username)
        return (await db.execute(query)).scalar_one_or_none()
    
    @staticmethod
    async def get_user_roles(user_id: str) -> List[str]:
        query = (
            select(Role.role_name)
            .join(UsersRole, Role.id == UsersRole.role_id)
            .where(UsersRole.users_id == user_id)
        )

        roles = (await db.execute(query)).scalars().all()
        return roles

    
    @staticmethod
    async def find_by_student_number(student_number: str):
        query = select(Users).where(Users.student_number == student_number)
        return (await db.execute(query)).scalar_one_or_none()

    
    @staticmethod
    async def find_by_user_id(user_id: str):
        query = select(Users).where(Users.id == user_id)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def find_by_email(email: str):
        query = select(Users).where(Users.email == email)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update_password(user: Users, password: str):
        user.password = password
        await db.commit()
