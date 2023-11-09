from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from app.config import db
from app.model.student import Student
from app.repository.base_repo import BaseRepo
from sqlmodel import Session



class StudentRepository(BaseRepo):
    model = Student
