
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo

from app.config import db
from app.schema import DefenseCreate, DefenseUpdate, ResponseSchema
from app.service.notif_service import NotificationService
from app.repository.notif_repo import NotificationRepository
from app.model import Notification

router = APIRouter(
    prefix="/notification",
    tags=['Notification for User'],
    dependencies=[Depends(JWTBearer())]
)



@router.get("/")
async def get_all_my_notif(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    user_id = token['user_id']
    try:
        return await NotificationService.display_my_notif(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Zero Notifications: {str(e)}")

@router.delete("/delete-all")
async def get_all_my_notif(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    user_id = token['user_id']
    try:
        return await NotificationService.delete_all_user_notif(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Zero Notifications: {str(e)}")
    

@router.delete("/delete/{notif_id}")
async def get_all_my_notif(notif_id: str,
                           credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
                           ):
    token = JWTRepo.extract_token(credentials)
    user_id = token['user_id']
    try:
        return await NotificationService.delete_selected(notif_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Zero Notifications: {str(e)}")