

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
    file_path: str
    research_adviser: str

    class Config:
        orm_mode = True

# ========================COMMENT
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

#==================STATUS

class StatusUpdate(BaseModel):
    status: Status

class CurrentUserResearchPaperResponse(ResearchPaperResponse):
    authors: Optional[List[AuthorSchema]] = []


#==================== ETHICS =====================
class EthicsCreate(BaseModel):
    research_paper_id: Optional[str]
    letter_of_intent: Optional[str]
    urec_9: Optional[str]
    urec_10: Optional[str]
    urec_11: Optional[str]
    urec_12: Optional[str]
    certificate_of_validation: Optional[str]
    co_authorship: Optional[str]
    research_paper_id: Optional[str]

class EthicsResponse(BaseModel):
    id: Optional[str]
    modified_at: Optional[datetime]
    created_at: Optional[datetime]
    letter_of_intent: Optional[str]
    urec_9: Optional[str]
    urec_10: Optional[str]
    urec_11: Optional[str]
    urec_12: Optional[str]
    certificate_of_validation: Optional[str]
    co_authorship: Optional[str]
    research_paper_id: Optional[str]
    status: str

class EthicsWithResearchResponse(BaseModel):
    id: Optional[str]
    modified_at: Optional[datetime]
    created_at: Optional[datetime]
    letter_of_intent: Optional[str]
    urec_9: Optional[str]
    urec_10: Optional[str]
    urec_11: Optional[str]
    urec_12: Optional[str]
    certificate_of_validation: Optional[str]
    co_authorship: Optional[str]
    research_paper_id: Optional[str]
    status: str

class EthicsUpdate(BaseModel):
    letter_of_intent: constr(strip_whitespace=True)
    urec_9: constr(strip_whitespace=True)
    urec_10: constr(strip_whitespace=True)
    urec_11: constr(strip_whitespace=True)
    urec_12: constr(strip_whitespace=True)
    certificate_of_validation: constr(strip_whitespace=True)
    co_authorship: constr(strip_whitespace=True)

# ===========================FULL MANUSCRIPT
class FullManuscriptCreate(BaseModel):
    research_paper_id: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    keywords: str = Field(..., min_length=1)
    abstract: str = Field(..., min_length=1)
    file: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)

    @validator('research_paper_id', 'content', 'keywords', 'abstract', 'file', 'status')
    def check_empty(cls, v):
        if v == "":
            raise ValueError("Field cannot be empty")
        return v

class FullManuscriptUpdate(BaseModel):
    content: constr(strip_whitespace=True)
    keywords: constr(strip_whitespace=True)
    file: constr(strip_whitespace=True)
    abstract: constr(strip_whitespace=True)
    status: constr(strip_whitespace=True)

class FullManuscriptResponse(BaseModel):
    id: Optional[str]
    modified_at: Optional[datetime]
    created_at: Optional[datetime]
    research_paper_id: Optional[str]
    content: Optional[str]
    keywords: Optional[str]
    abstract: Optional[str]
    file: Optional[str]
    status: Optional[str]

class FullManuscriptWithResearchResponse(BaseModel):
    id: Optional[str]
    modified_at: Optional[datetime]
    created_at: Optional[datetime]
    research_paper_id: Optional[str]
    content: Optional[str]
    keywords: Optional[str]
    abstract: Optional[str]
    file: Optional[str]
    status: Optional[str]
    title: str  # Add this line to include the title attribute

# =============================END

# =========================COPYRIGHT =================
class CopyRightCreate(BaseModel):
    research_paper_id: Optional[str]
    co_authorship: Optional[str]
    affidavit_co_ownership: Optional[str]
    joint_authorship: Optional[str]
    approval_sheet: Optional[str]
    receipt_payment: Optional[str]
    recordal_slip: Optional[str]
    acknowledgement_receipt: Optional[str]
    certificate_copyright: Optional[str]
    recordal_template: Optional[str]
    ureb_18: Optional[str]
    journal_publication: Optional[str]
    copyright_manuscript: Optional[str]


class CopyRightUpdate(BaseModel):
    co_authorship: constr(strip_whitespace=True)
    affidavit_co_ownership: constr(strip_whitespace=True)
    joint_authorship: constr(strip_whitespace=True)
    approval_sheet: constr(strip_whitespace=True)
    receipt_payment: constr(strip_whitespace=True)
    recordal_slip: constr(strip_whitespace=True)
    acknowledgement_receipt: constr(strip_whitespace=True)
    certificate_copyright: constr(strip_whitespace=True)
    recordal_template: constr(strip_whitespace=True)
    ureb_18: constr(strip_whitespace=True)
    journal_publication: constr(strip_whitespace=True)
    copyright_manuscript: constr(strip_whitespace=True)

class CopyRightResponse(BaseModel):
    id: Optional[str]
    modified_at: Optional[datetime]
    created_at: Optional[datetime]
    research_paper_id: Optional[str]
    co_authorship: Optional[str]
    affidavit_co_ownership: Optional[str]
    joint_authorship: Optional[str]
    approval_sheet: Optional[str]
    receipt_payment: Optional[str]
    recordal_slip: Optional[str]
    acknowledgement_receipt: Optional[str]
    certificate_copyright: Optional[str]
    recordal_template: Optional[str]
    ureb_18: Optional[str]
    journal_publication: Optional[str]
    copyright_manuscript: Optional[str]
    status: str

class CopyRightWithResearchResponse(BaseModel):
    id: Optional[str]
    modified_at: Optional[datetime]
    created_at: Optional[datetime]
    research_paper_id: Optional[str]
    co_authorship: Optional[str]
    affidavit_co_ownership: Optional[str]
    joint_authorship: Optional[str]
    approval_sheet: Optional[str]
    receipt_payment: Optional[str]
    recordal_slip: Optional[str]
    acknowledgement_receipt: Optional[str]
    certificate_copyright: Optional[str]
    recordal_template: Optional[str]
    ureb_18: Optional[str]
    journal_publication: Optional[str]
    copyright_manuscript: Optional[str]
    status: str
    title: str
# ------------ RESPONSE FOR ALL ETHICS< MANU< COPYRIGHT ---------------


# ================ FOR SHOWING
class EthicsSchema(BaseModel):
    letter_of_intent: Optional[str]
    urec_9: Optional[str]
    urec_10: Optional[str]
    urec_11: Optional[str]
    urec_12: Optional[str]
    certificate_of_validation: Optional[str]
    co_authorship: Optional[str]

class FullManuscriptSchema(BaseModel):
    content: str
    keywords: str
    file: str
    abstract: str
    status: str

class CopyrightSchema(BaseModel):
    co_authorship: Optional[str]
    affidavit_co_ownership: Optional[str]
    joint_authorship: Optional[str]
    approval_sheet: Optional[str]
    receipt_payment: Optional[str]
    recordal_slip: Optional[str]
    acknowledgement_receipt: Optional[str]
    certificate_copyright: Optional[str]
    recordal_template: Optional[str]
    ureb_18: Optional[str]
    journal_publication: Optional[str]
    copyright_manuscript: Optional[str]
class DisplayAllByUser(BaseModel):
    research_paper_id: str
    title: str
    research_type: str
    submitted_date: str
    status: str
    file_path: str
    research_adviser: str
    ethics: Optional[EthicsSchema]
    full_manuscript: Optional[FullManuscriptSchema]
    copyright: Optional[CopyrightSchema]



#FOR THE DISPLAY OF LIST IN PAGE
class PageResponse(GenericModel, Generic[T]):
    """ The response for a pagination query. """

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]
