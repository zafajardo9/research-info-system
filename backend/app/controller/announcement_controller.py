from typing import List
from fastapi import APIRouter, Depends, Path, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.future import select
from app.repository.auth_repo import JWTBearer, JWTRepo



from app.schema import ResponseSchema, AnnouncementCreate, AnnouncementDisplay
from app.service.announcement_service import AnnouncementService
from app.model.announcements import Announcement

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

@router.get("/announcements_with_user_names/", response_model=List[AnnouncementDisplay])
async def get_announcements_with_user_names():
    announcements = await AnnouncementService.get_announcements_with_user_names()
    return announcements