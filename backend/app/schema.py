

from datetime import datetime
from fastapi import HTTPException
import logging
import re
from typing import List, TypeVar, Optional, Generic

from pydantic.generics import GenericModel
from pydantic import BaseModel, Field, validator, constr
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
    
    
# ================================================================
class ResearchPaperCreate(BaseModel):
    title: str
    research_type: str
    file_path: str
    submitted_date: str
    research_adviser: str

# ================ FOR SHOWING
class AuthorShow(BaseModel):
    user_id: str
    student_name: str
    student_year: int
    student_section: str
    student_course: str
    student_number: str
    student_phone_number: str

class ResearchPaperShow(BaseModel):
    id: str
    title: str
    research_type: str
    submitted_date: str
    status: str
    file_path: str
    research_adviser: str

    class Config:
        orm_mode = True

class ResearchPaperWithAuthorsResponse(BaseModel):
    research_paper: ResearchPaperShow
    authors: List[AuthorShow]

    class Config:
        orm_mode = True

#==========================



class AuthorResponse(BaseModel):
    id: Optional[str]
    user_id: str
    research_paper_id: str

class ResearchPaperResponse(BaseModel):
    id: Optional[str]
    title: str
    research_type: str
    submitted_date: str
    status: str
    file_path: str
    research_adviser: str

    class Config:
        orm_mode = True



class ResearchEdit(BaseModel):
    title: str
    research_type: str
    submitted_date: str
<<<<<<< HEAD
=======
    keywords: str
    #status: str
>>>>>>> 6bef47d3855f4eb655bd95dbc23fb08efbd2cb40
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


#==================== ETHICS =====================
class EthicsCreate(BaseModel):
    research_paper_id: str
    letter_of_intent: str
    urec_9: str
    urec_10: str
    urec_11: str
    urec_12: str
    certificate_of_validation: str
    co_authorship: str
    research_paper_id: str

class EthicsResponse(BaseModel):
    created_at: datetime
    letter_of_intent: str
    urec_9: str
    urec_10: str
    urec_11: str
    urec_12: str
    certificate_of_validation: str
    co_authorship: str
    research_paper_id: str

class EthicsUpdate(BaseModel):
    letter_of_intent: constr(strip_whitespace=True)
    urec_9: constr(strip_whitespace=True)
    urec_10: constr(strip_whitespace=True)
    urec_11: constr(strip_whitespace=True)
    urec_12: constr(strip_whitespace=True)
    certificate_of_validation: constr(strip_whitespace=True)
    co_authorship: constr(strip_whitespace=True)

    



#FOR THE DISPLAY OF LIST IN PAGE
class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]
