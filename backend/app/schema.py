

from datetime import datetime
from fastapi import HTTPException
import logging
import re
from typing import List, TypeVar, Optional, Generic

from pydantic.generics import GenericModel
from pydantic import BaseModel, Field, validator
from sqlalchemy import false

from app.model.research_paper import Author, Status


T = TypeVar('T')

# get root logger
logger = logging.getLogger(__name__)


class RegisterSchema(BaseModel):

    username: str
    email: str
    name: str
    password: str
    
    year: int
    section: str
    course: str
    
    phone_number: str
    student_number: str
    birth: str

    # phone number validation

    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validatior: {v}")

        # regex phone number
        regex = r"^09[0-9]{9}$"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail="Invalid input phone number!")
        return v


class RegisterSchemaFaculty(BaseModel):

    username: str
    email: str
    name: str
    password: str
    
    phone_number: str
    birth: str

    # phone number validation

    @validator("phone_number")
    def phone_validation(cls, v):
        logger.debug(f"phone in 2 validatior: {v}")

        # regex phone number
        regex = r"^09[0-9]{9}$"
        if v and not re.search(regex, v, re.I):
            raise HTTPException(status_code=400, detail="Invalid input phone number!")
        return v


class LoginSchema(BaseModel):
    username: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str


class DetailSchema(BaseModel):
    status: str
    message: str
    result: Optional[T] = None


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None

class AuthorSchema(BaseModel):
    user_id: int
    research_paper_id: int
    
    

class ResearchPaperCreate(BaseModel):
    title: str
    content: str
    abstract: str
    research_type: str 
    keywords: str
    file_path: str
    submitted_date: str
    research_adviser: str


# class ResearchPaperResponse(BaseModel):
#     id: Optional[str]
#     title: str
#     content: str
#     abstract: str
#     research_type: str
#     submitted_date: str
#     status: str
#     keywords: str
#     file_path: str
#     research_adviser: str

#     class Config:
#         orm_mode = True


class AuthorResponse(BaseModel):
    id: Optional[str]
    user_id: str
    research_paper_id: str

class ResearchPaperResponse(BaseModel):
    id: Optional[str]
    title: str
    content: str
    abstract: str
    research_type: str
    submitted_date: str
    status: str
    keywords: str
    file_path: str
    research_adviser: str

    class Config:
        orm_mode = True



class ResearchEdit(BaseModel):
    title: str
    content: str
    abstract: str
    research_type: str
    submitted_date: str
    keywords: str
    file_path: str
    research_adviser: str

    class Config:
        orm_mode = True


class ResearchComment(BaseModel):
    text: str
    research_id: str

class ResearchCommentResponse(BaseModel):
    created_at: datetime
    id: str
    text: str
    user_id: str
    name: str
    research_paper_id: str

    class Config:
        orm_mode = True


class StatusUpdate(BaseModel):
    status: Status

class CurrentUserResearchPaperResponse(ResearchPaperResponse):
    authors: Optional[List[AuthorSchema]] = []





#FOR THE DISPLAY OF LIST IN PAGE
class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]
