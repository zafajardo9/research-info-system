from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from app.config import db
from app.model.research_paper import ResearchPaper
from app.repository.base_repo import BaseRepo


class ResearchPaperRepository(BaseRepo):
    model = ResearchPaper


