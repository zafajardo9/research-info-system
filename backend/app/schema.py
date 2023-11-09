

from fastapi import HTTPException
import logging
import re
from typing import List, TypeVar, Optional, Generic

from pydantic.generics import GenericModel
from pydantic import BaseModel, validator
from sqlalchemy import false


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
    name: str
    
    

class ResearchPaperSchema(BaseModel):
    title: str
    content: str
    research_adviser: int
        



#FOR THE DISPLAY OF LIST IN PAGE
class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]
