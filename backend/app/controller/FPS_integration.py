from typing import List, Optional
from app.repository.research_repo import ResearchPaperRepository
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import FPSTest, ResponseSchema
from app.config import db
from app.service.all_about_info_service import AllInformationService
from app.repository.users import UsersRepository
from app.service.research_service import ResearchService
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure the root logger to print logs to the console
logging.basicConfig(level=logging.DEBUG)

# Optionally, configure a file handler to save logs to a file
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(file_handler)

router = APIRouter(
    prefix="/integration",
    tags=['All related to integration'],
    dependencies=[Depends(JWTBearer())]
)

# @router.post("/fps/upload-all")
# async def testing_fps(research_paper_data: List[FPSTest]):

#     try:
#         faculty_papers = await ResearchService.upload_multiple_faculty_papers(research_paper_data)
#         return ResponseSchema(detail="All research papers created successfully", result=[faculty_paper.dict() for faculty_paper in faculty_papers])
#     except ValueError as ve:
#         return ResponseSchema(detail=f"Error creating research paper: Invalid date format. Please use 'dd-mm-yyyy'.", result=None)
#     except HTTPException as e:
#         return ResponseSchema(detail=f"Error creating research paper: {str(e)}", result=None)




@router.get("/faculty/research-papers/list")
async def list_of_papers():
    try:
        research_papers = await ResearchService.for_FPS_integration()
        if research_papers:
            return research_papers
        else:
            return None
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        return ResponseSchema(detail=f"SQLAlchemy Error retrieving research papers: {str(e)}", result=None)
    except HTTPException as e:
        # Handle FastAPI HTTPException
        return ResponseSchema(detail=f"FastAPI Error retrieving research papers: {str(e)}", result=None)
    except Exception as e:
        # Handle other unexpected errors
        logging.exception(f"Error in API LOGGED: {str(e)}")
        return ResponseSchema(detail=f"Unexpected Error retrieving research papers: {str(e)}", result=None)


@router.get("/alumni/{student_number}/papers/")
async def list_of_papers(student_number: str):
    try:
        result = await ResearchService.get_alumni_papers(student_number)
        if result:
            return result
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)
    
    
# @router.get("/accre/list/papers")
# async def list_of_papers():
#     try:
#         result = await ResearchService.get_all_research_with_authors_info_integration()
#         if result:
#             return result
#         else:
#             return None
#     except HTTPException as e:
#         return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)
    


@router.get("/accre/all-papers")
async def list_of_papers():
    try:
        result = await ResearchPaperRepository.accre_combine()
        if result:
            return result
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)
    
    
@router.get("/accre/all-papers/faculty")
async def list_of_papers():
    try:
        result = await ResearchPaperRepository.accre_get_faculty()
        if result:
            return result
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)


@router.get("/accre/all-papers/students")
async def list_of_papers():
    try:
        research_papers = await ResearchPaperRepository.accre_get_student()
        if research_papers is None:
            return []
        return research_papers
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting research papers: {str(e)}", result=None)
    
@router.get("/accre/lists")
async def list_of_papers(
    user_type: Optional[str] = None
):
    try:
        research_papers = await ResearchPaperRepository.accre_pagination(user_type)
        if research_papers is None:
            return []
        return research_papers
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting research papers: {str(e)}", result=None)
    
    



@router.get("/extension/for-extension/list")
async def extension_list_for_extension():
    try:
        research_papers = await ResearchService.extension_list_for_extension()
        if research_papers is None:
            return []
        return research_papers
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting records: {str(e)}", result=None)

@router.get("/extension/from-extension/list")
async def extension_list_for_extension():
    try:
        research_papers = await ResearchService.extension_list_for_extension()
        if research_papers is None:
            return []
        return research_papers
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting records: {str(e)}", result=None)







