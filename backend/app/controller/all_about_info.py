from typing import List
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import ResponseSchema
from app.config import db
from app.service.all_about_info_service import AllInformationService

router = APIRouter(
    prefix="/info",
    tags=['All Information For analytics'],
    #dependencies=[Depends(JWTBearer())]
)


@router.get("/student_count/all")
async def read_student_count_all():
    count = await AllInformationService.get_student_count_all(db)
    return {"Number": "All Students", "student_count": count}



@router.get("/student_count/{course}")
async def read_student_count(course: str):
    count = await AllInformationService.get_student_count_by_course(db, course)
    return {"course": course, "student_count": count}

@router.get("/student_count/{course}/{section}")
async def read_student_count_by_course_section(course: str, section: str):
    count = await AllInformationService.read_student_count_by_course_section(db, course, section)
    return {"course": course, "section": section, "student_count": count}


@router.get("/research_count_by_type/all")
async def read_research_count_by_type():
    counts = await AllInformationService.get_number_of_research_by_type(db)
    return counts

#Number or Research
@router.get("/research_proposal_count/all")
async def read_research_count_all():
    count = await AllInformationService.get_number_of_research_proposal(db)
    return {"Number": "All Research", "Research Count": count}


@router.get("/research_proposal_count_based_status/all")
async def read_research_count_all():
    counts = await AllInformationService.get_number_of_research_proposal_by_approve(db)
    return counts


@router.get("/ethics_count/all")
async def read_research_count_all():
    counts = await AllInformationService.get_number_ethics(db)
    return {"Ethics Count": counts}


@router.get("/ethics_count/all")
async def read_research_count_all():
    counts = await AllInformationService.get_number_ethics(db)
    return {"Ethics Count": counts}

@router.get("/manuscript_count/all")
async def read_research_count_all():
    counts = await AllInformationService.get_number_manuscript(db)
    return {"Manuscript Count": counts}

@router.get("/copyright_count/all")
async def read_research_count_all():
    counts = await AllInformationService.get_number_copyright(db)
    return {"Copyright Count": counts}


@router.get("/research_status/{course}/{section}")
async def get_research_status_by_course_section(course: str = Path(..., title="The course of the student", min_length=1),
                                section: str = Path(..., title="The section of the student", min_length=1)):
    status = await AllInformationService.get_research_status_by_course_section(db, course, section)
    return {"Course": course, "Section": section, "Research Status": status}


#FOR RESEARCH ADVISER ================= INFOR ABOUT THE RESEARCH  papers they are under to

# @router.get("/adviser/number-of-my-advisory")
# async def get_research_status_by_course_section(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    
#     token = JWTRepo.extract_token(credentials)
#     current_user = token['user_id']
#     count = await AllInformationService.get_number_of_my_advisory(db, current_user)
#     return {"My advisory count": count}

@router.get("/number-of-advisory-by-status/{status}")
async def get_number_of_advisory_by_status(
    status: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    count = await AllInformationService.get_number_of_advisory_by_status(db, current_user, status)
    return {"Status": status, "Count" : count}


@router.get("/number-of-advisory-by-status")
async def get_number_of_advisory_by_status(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    number_pending = await AllInformationService.get_number_of_advisory_by_status(db, current_user, "Pending")
    number_approve = await AllInformationService.get_number_of_advisory_by_status(db, current_user, "Approve")
    number_reject = await AllInformationService.get_number_of_advisory_by_status(db, current_user, "Reject")
    total_number = await AllInformationService.get_number_of_my_advisory(db, current_user)
    return {
        "Pending": {
            "Advisory count": number_pending,
        },
        "Approve": {
            "Advisory count": number_approve,
        },
        "Reject": {
            "Advisory count": number_reject,
        },
        "Number of my advisory": total_number
        
        
        }