from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db
from app.model.research_status import Comment
from app.repository.base_repo import BaseRepo
from app.model.users import Users, Role
from typing import List, Dict



class RoleRepository(BaseRepo):
    model = Role


    @staticmethod
    async def find_by_role_name(role_name:str):
        query = select(Role).where(Role.role_name == role_name)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def find_by_list_role_name(role_name:List[str]):
        query =  select(Role).where(Role.role_name.in_(role_name))
        return (await db.execute(query)).scalars().all()

    @staticmethod
    async def create_list(role_name: List[Role]):
        db.add_all(role_name)
        await commit_rollback()