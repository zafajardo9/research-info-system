from typing import List, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.service.research_service import ResearchService
from app.config import db
from app.repository.users import UsersRepository
from app.schema import ResponseSchema


from app.service.users_service import UserService
from app.repository.users import UsersRepository

router = APIRouter(
    prefix="/admin",
    tags=['Admin Power'],
    dependencies=[Depends(JWTBearer())]
)

@router.post("/assign-roles/{user_id}")
async def assign_roles(
    user_id: str,
    assigned_roles: List[str],
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
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



@router.get("/users_faculty_with_roles", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_users_with_roles(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    """
    Get all users with their roles
    """
    token = JWTRepo.extract_token(credentials)
    user_roles = token.get('role', [])

    if "admin" not in user_roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")

    result = await UserService.get_all_in_faculty_with_roles()
    
    if result:
        formatted_result = UserService.format_users_with_roles(result)
        return ResponseSchema(detail="Successfully fetched user profiles with roles!", result=formatted_result)
    else:
        raise HTTPException(status_code=404, detail="User list not found")
    
    