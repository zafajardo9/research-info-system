from datetime import datetime
import math
from typing import List, Optional
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.config import commit_rollback, db

from sqlalchemy.orm import joinedload
from app.model.users import Users
from app.model.assignedTo import AssignedResearchType, AssignedSections
from app.repository.base_repo import BaseRepo
from app.schema import AssignWhole

class AssignedResearchTypeRepository(BaseRepo):
    model = AssignedResearchType
    
    
    
    
    
    # =============================#============================#
class AssignedSectionsRepository(BaseRepo):
    model = AssignedSections