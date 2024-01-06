from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from app.config import db
from app.model.workflowprocess import Workflow, WorkflowStep
from app.model import NavigationClass
from app.repository.base_repo import BaseRepo
from sqlalchemy.orm import joinedload

class NavigationClassRepository(BaseRepo):
    model = NavigationClass

