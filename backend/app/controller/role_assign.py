from operator import itemgetter
from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from itertools import groupby

from app.repository.auth_repo import JWTBearer, JWTRepo



from app.config import db

#from app.schema import WorkflowCreate

router = APIRouter(
    prefix="/roles",
    tags=['Assigning Roles to user'],
    dependencies=[Depends(JWTBearer())]
)

# ==========================PROCESS NAVIGATION FOR ADVISER AND PROFESSOR=============================================================
