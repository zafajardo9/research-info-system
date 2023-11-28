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
from app.model.users import Users, UsersRole
from typing import List, Dict



class UserRoleRepository(BaseRepo):
    model = UsersRole
