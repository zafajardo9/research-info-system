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
    tags=['All Information'],
    dependencies=[Depends(JWTBearer())]
)


@router.get("/student_count/all")
async def read_student_count_all():
    count = await AllInformationService.get_student_count_all(db)
    return {"Number": "All Students", "student_count": count}



@router.get("/student_count/{course}")
async def read_student_count(course: str):
    count = await AllInformationService.get_student_count_by_course(db, course)
    return {"course": course, "student_count": count}


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

@router.get("/manuscript_count/all")
async def read_research_count_all():
    counts = await AllInformationService.get_number_manuscript(db)
    return {"Manuscript Count": counts}

@router.get("/copyright_count/all")
async def read_research_count_all():
    counts = await AllInformationService.get_number_copyright(db)
    return {"Copyright Count": counts}