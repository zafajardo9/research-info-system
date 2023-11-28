from typing import List, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.service.research_service import ResearchService
from app.config import db
from app.repository.users import UsersRepository

router = APIRouter(
    prefix="/admin",
    tags=['Admin Power'],
    dependencies=[Depends(JWTBearer())]
)

@router.post("/assign-roles/{user_id}")
async def assign_roles(
    user_id: str,
    assigned_roles: list[str],
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):

    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign roles to the user
    await UsersRepository.assign_roles(user_id, assigned_roles)

    return {"message": f"Roles assigned to user with ID {user_id}"}
