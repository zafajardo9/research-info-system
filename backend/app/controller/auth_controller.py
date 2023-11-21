from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.service.author_service import AuthorService
from app.model.research_paper import Author
from app.schema import AuthorSchema, ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.service.users_service import UserService
from app.config import db

router = APIRouter(
    prefix="/author",
    tags=['Author'],
    dependencies=[Depends(JWTBearer())]
)

@router.post("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_author(
    author_data: AuthorSchema,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    username = token['username']

    # Get user_id by username
    user_id = await UserService.get_student_profile(username)

    # Link the author with the current user
    author_data.user_id = user_id

    return await AuthorService.create_author(db, author_data)

@router.get("/{author_id}", response_model=Author)
async def read_author(author_id: str):
    '''FOR STUDENTS'''
    result = await UserService.get_student_profile(author_id)
    if result:
        return ResponseSchema(detail="Successfully fetch student profile!", result=result)
    else:
        raise HTTPException(status_code=404, detail="Student profile not found")


