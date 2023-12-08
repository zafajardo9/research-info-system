from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.config import db


from app.schema import ResponseSchema, AnnouncementCreate, AnnouncementDisplay
from app.service.announcement_service import AnnouncementService
from app.model.announcements import Announcement
from app.repository.announcement_repo import AnnouncementRepository

#from app.schema import WorkflowCreate

router = APIRouter(
    prefix="/announcement",
    tags=['Making and Displaying Announcements'],
    dependencies=[Depends(JWTBearer())]
)



@router.post("/create/", response_model=Announcement)
async def assign_section(
        data: AnnouncementCreate,
        credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    roles = token.get('role', [])
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to assign.")

    assignUser = await AnnouncementService.create_announcement(data, current_user)

    return assignUser

@router.get("/announcements_with_user_names/")
async def get_announcements_with_user_names():
    announcements = await AnnouncementService.get_announcements_with_user_names()
    return announcements


@router.delete("/delete_announcement/{id}")
async def delete_announcement_by_id(id: str):
    announcements = await AnnouncementService.delete_announcement_by_id(id)
    if announcements:
        return {"message": "Announcement deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Announcement not found")


@router.delete("/delete_all_announcement")
async def delete_all_announcement():
    announcements = await AnnouncementService.delete_all_announcements_function()
    if announcements:
        return {"message": "All Announcement deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Announcement not found")


# ============== STUDENT
@router.get("/announcements_for-student/FundingOpportunity")
async def get_announcements_students_funding():
    announcements = await AnnouncementService.get_announcements_students_funding()
    if announcements:
        return announcements
    else:
        return {"message": "No announcements found for students with training or workshop type."}

@router.get("/announcements_for-student/Training&Workshop")
async def get_announcements_students_training():
    announcements = await AnnouncementService.get_announcements_students_training()
    
    if announcements:
        return announcements
    else:
        return {"message": "No announcements found for students with training or workshop type."}
    
    
# ============ FACULTY
@router.get("/announcements_for-faculty/FundingOpportunity")
async def get_announcements_students_funding():
    announcements = await AnnouncementService.get_announcements_faculty_funding()
    if announcements:
        return announcements
    else:
        return {"message": "No announcements found for faculty with training or workshop type."}

@router.get("/announcements_for-faculty/Training&Workshop")
async def get_announcements_students_training():
    announcements = await AnnouncementService.get_announcements_faculty_training()
    
    if announcements:
        return announcements
    else:
        return {"message": "No announcements found for faculty with training or workshop type."}
