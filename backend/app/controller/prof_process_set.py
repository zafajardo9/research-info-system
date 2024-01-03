from operator import itemgetter
from typing import List
import uuid
from fastapi import APIRouter, Depends, Path, Security, HTTPException, logger
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.schema import AssignUserProfile, AssignWhole, AssignedResearchTypeCreate, AssignedSectionsCreate, NavigationTabCreate, NavigationTabUpdate, ResponseSchema, UpdateAssign, UpdateResearchTypeAssign, UserWithAssignments, WorkflowCreate, WorkflowCreateWithSteps, WorkflowDetail, WorkflowGroupbyType, WorkflowStepCreate, WorkflowStepDetail
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
from app.model.workflowprocess import NavigationClass, NavigationTab

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
async def update_process_role(id: str, navigation_tab_update: NavigationTabUpdate):
    updated_process = await WorkflowService.update_process_role(id, navigation_tab_update)
    return updated_process

@router.post("/add-more-class/{nav_id}")
async def insert_more(nav_id: str, class_ids: List[str]):
    try:
        # Retrieve the navigation record
        navigation_record = await db.execute(select(NavigationTab).where(NavigationTab.id == nav_id))
        navigation_record = navigation_record.scalar()

        if not navigation_record:
            raise HTTPException(status_code=404, detail=f"Navigation with id {nav_id} not found.")

        # Insert new class entries for the navigation
        for class_id in class_ids:
            navigation_class_entry = NavigationClass(id=str(uuid.uuid4()), navigation_id=nav_id, class_id=class_id)
            db.add(navigation_class_entry)

        await db.commit()

        return {"message": f"Classes added to navigation with id {nav_id} successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# =====================================
@router.delete("/delete-assigned-process/{id}")
async def update_process_role(id: str):
    delete = await WorkflowService.delete_process_by_id(id)
    if not delete:
        raise HTTPException(status_code=404, detail="Process not found")

    return {"message": "Process deleted successfully"}


@router.delete("/delete-assigned-class/{id}")
async def update_process_role(id: str):
    delete = await WorkflowService.delete_assign_class(id)
    if not delete:
        raise HTTPException(status_code=404, detail="Class not found")

    return {"message": "Process deleted successfully"}
# ==============================================
    
@router.get("/display-all/")
async def display_process_all():
    '''Wala to like as in same lang nung query sa Database SELECT * FROM'''
    results = await WorkflowService.display_process()
    return results
    
@router.get("/display-process-all/{type}")
async def display_process_by_type(
    type: str
):
    '''Ito may Format pero pwede ka mag req ano pinakamaganda'''
    results = await WorkflowService.display_process_by_type(type)
    return results
