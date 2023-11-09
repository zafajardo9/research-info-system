from sqlalchemy.future import select
from app.config import db
from app.model.faculty import Faculty
from app.repository.base_repo import BaseRepo

class FacultyRepository(BaseRepo):
    model = Faculty

