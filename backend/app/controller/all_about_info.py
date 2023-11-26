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

# async def read_research_count_all(course: str):
#     count = await AllInformationService.get_number_of_research_proposal(db)
#     return {"course": course, "student_count": count}


