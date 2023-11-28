from typing import List, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import ResponseSchema
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
    roles: list[str],
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):

    token = JWTRepo.extract_token(credentials)
    roles = token.get('role', [])

    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only Admins are allowed.")
    user = await UsersRepository.find_by_user_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Assign roles to the user
    await UsersRepository.assign_roles(user_id, roles)

    return {"message": f"Roles assigned to user with ID {user_id}"}

# @router.put("/select_process/", response_model=ResponseSchema, response_model_exclude_none=True)
# async def make_process(
#     research_paper_id: str,
#     status_update: StatusUpdate,
#     credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
# ):
#     # Extract the user role from the JWT token
#     token = JWTRepo.extract_token(credentials)
#     current_user_role = token['role'] #this line will show what role the logged in user is

#     is_allowed = await ResearchService.check_faculty_permission(current_user_role)
#     if not is_allowed:
#         raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper. Your role is {current_user_role}.")
#     # Update the status
#     try:
#         research_paper = await ResearchService.update_research_paper_status(db, research_paper_id, status_update.status)
#         return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
#     except HTTPException as e:
#         return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)
