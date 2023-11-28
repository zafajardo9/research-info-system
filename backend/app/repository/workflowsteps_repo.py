
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from app.config import db
from app.model.workflowprocess import WorkflowStep
from app.repository.base_repo import BaseRepo

class WorkflowStepRepository(BaseRepo):
    model = WorkflowStep
