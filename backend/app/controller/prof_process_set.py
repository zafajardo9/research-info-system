from operator import itemgetter
from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, NavigationTabCreate, ResponseSchema, UpdateAssign, UpdateResearchTypeAssign, UserWithAssignments, WorkflowCreate, WorkflowCreateWithSteps, WorkflowDetail, WorkflowGroupbyType, WorkflowStepCreate, WorkflowStepDetail
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.repository.workflow_repo import WorkflowRepository
from app.repository.workflowsteps_repo import WorkflowStepRepository
from app.model import Workflow, WorkflowStep, AssignedResearchType, AssignedSections
from app.service.workflow_service import WorkflowService
from app.service.assignTo_service import AssignToSection
from app.service.users_service import UserService
from app.repository.users import UsersRepository
from app.model.users import Users
from itertools import groupby


from app.config import db
from app.model.faculty import Faculty
from app.model.workflowprocess import NavigationTab

#from app.schema import WorkflowCreate

router = APIRouter(
    prefix="/faculty_process",
    tags=['Creating Process For Faculty'],
    dependencies=[Depends(JWTBearer())]
)

# ==========================PROCESS NAVIGATION FOR ADVISER AND PROFESSOR=============================================================

faculty_process_name = {
    1 : "Submitted Proposal",
    2 : "Pre-Oral Defense Date",
    3 : "Submitted Ethics/Protocol",
    4 : "Submitted Full Manuscript",
    5 : "Set Final Defense Date",
    6 : "Submitted Copyright"
}


@router.get("/process-list-name")
async def list_of_process_for_faculty():
    '''Can be use in dropdown list'''
    return faculty_process_name

@router.post("/assign-process/")
async def create_process_role(navigation_tab: NavigationTabCreate):
    create_process = await WorkflowService.create_process_role(navigation_tab)
    return create_process


@router.put("/update-assigned-process/{id}")
async def update_process_role(id: str, navigation_tab: NavigationTabCreate):
    updated_process = await WorkflowService.update_process_role(id, navigation_tab)
    return updated_process

@router.delete("/delete-assigned-process/{id}")
async def update_process_role(id: str):
    delete = await WorkflowService.delete_process_by_id(id)
    if not delete:
        raise HTTPException(status_code=404, detail="Process not found")

    return {"message": "Process deleted successfully"}

    
@router.get("/display-all/")
async def display_process_all():
    '''Wala to like as in same lang nung query sa Database SELECT * FROM'''
    results = await WorkflowService.display_process()
    return results
    
@router.get("/display-process-all/type")
async def display_process_by_type():
    '''Ito may Format pero pwede ka mag req ano pinakamaganda'''
    results = await WorkflowService.display_process_by_type()
    return results
