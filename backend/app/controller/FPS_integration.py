from typing import List
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import ResponseSchema
from app.config import db
from app.service.all_about_info_service import AllInformationService
from app.repository.users import UsersRepository
from app.service.research_service import ResearchService

router = APIRouter(
    prefix="/integration",
    tags=['All related to integration']
)




@router.get("/faculty/research-papers/list")
async def list_of_papers():
    try:
        research_papers = await ResearchService.for_FPS_integration()
        if research_papers:
            return research_papers
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)
    



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
    
    
@router.get("/accre/list/papers")
async def list_of_papers():
    try:
        result = await ResearchService.get_all_research_with_authors_info_integration()
        if result:
            return result
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)
    
    


@router.get("/extension/for-extension/list")
async def extension_list_for_extension():
    try:
        research_papers = await ResearchService.extension_list_for_extension()
        if research_papers is None:
            return []
        return research_papers
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting records: {str(e)}", result=None)




