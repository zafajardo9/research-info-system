from typing import List
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import ResponseSchema
from app.config import db
from app.service.all_about_info_service import AllInformationService
from app.repository.users import UsersRepository

router = APIRouter(
    prefix="/info",
    tags=['All Information For analytics'],
    #dependencies=[Depends(JWTBearer())]
)


#FOR ADMIN

@router.get("/student_count/")
async def read_student_count():
    total_count_student = await AllInformationService.get_student_count_all(db)
    list_course = await UsersRepository.filter_student_year_course()
    
    
    result = [{"Total Number of STUDENTS": total_count_student}]
    for course_item in list_course:
        count = await AllInformationService.read_student_count_by_course_section(db, course_item.course, course_item.section)
        result.append({"course": course_item.course, "section": course_item.section, "student_count": count})



    return result



@router.get("/research_count_by_type/all")
async def read_research_count_by_type():
    counts = await AllInformationService.get_number_of_research_by_type(db)
    return counts



@router.get("/research_proposal_count_based_status/all")
async def read_research_count_all():
    counts = await AllInformationService.get_number_of_research_proposal_by_approve(db)
    return counts


@router.get("/admin/count-research-info/all")
async def read_research_count_all():
    research_count = await AllInformationService.get_number_of_research_proposal(db)
    ethics_counts = await AllInformationService.get_number_ethics(db)
    manuscript_count = await AllInformationService.get_number_manuscript(db)
    copyright_count = await AllInformationService.get_number_copyright(db)
    return {
        "Research Count": research_count,
        "Ethics Count": ethics_counts,
        "Manuscript Count": manuscript_count,
        "Copyright Count": copyright_count,
        }


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
    
    ## dagdagan to base sa status dapat
    return {"Status": status, "Count" : count}


@router.get("/number-of-advisory-by-status")
async def get_number_of_advisory_by_status(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''Shows data about research paper under'''
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    total_number = await AllInformationService.get_number_of_my_advisory(db, current_user)
    ethics_count = await AllInformationService.get_number_of_ethics_by_adviser(db, current_user)
    copyright_count = await AllInformationService.get_number_of_copyright_by_adviser(db, current_user)
    manuscript_count = await AllInformationService.get_number_of_full_manuscript_by_adviser(db, current_user)
    
    
    proposal_status_count = await AllInformationService.get_status_count_of_proposal_by_adviser(db, current_user)
    ethics_status_count = await AllInformationService.get_status_count_of_ethics_by_adviser(db, current_user)
    copyright_status_count = await AllInformationService.get_status_count_of_copyright_by_adviser(db, current_user)
    manuscript_status_count = await AllInformationService.get_status_count_of_full_manuscript_by_adviser(db, current_user)
    return {
        "Number of my advisory": total_number,
        "PROPOSALS": {
            "Proposal Status Counts": proposal_status_count,
        },
        "ETHICS": {
            "COUNT OF SUBMITTED" : ethics_count,
            "Ethics Status Counts": ethics_status_count,
        },
        
        "COPYRIGHT": {
            "COUNT OF SUBMITTED": copyright_count,
            "Copyright Status Counts": copyright_status_count,
        },
        "FULL MANUSCRIPT": {
            "COUNT OF SUBMITTED": manuscript_count,
            "Manuscript Status Counts": manuscript_status_count,
        }
    }