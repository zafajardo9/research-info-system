
from typing import List, Optional
from sqlalchemy.sql import select
from uuid import uuid4
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.service.research_service import ResearchService
from app.schema import DisplayAllByUser, ResearchEdit, ResearchPaperCreate, ResearchPaperResponse, ResearchPaperWithAuthorsResponse, ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from datetime import datetime

from app.config import db
from app.repository.research_repo import ResearchPaperRepository
from app.model import Users, Author, ResearchPaper
from app.service.users_service import UserService
from app.model.research_paper import FacultyResearchPaper, Status
from app.service.workflow_service import WorkflowService

router = APIRouter(
    prefix="/research",
    tags=['Research'],
    dependencies=[Depends(JWTBearer())]
)


@router.post("/upload", response_model=ResponseSchema, response_model_exclude_none=True)
async def upload_research_paper(
    research_paper_data: ResearchPaperCreate,
    author_ids: List[str],
):
    try:
        research_paper = await ResearchService.create_research_paper(db, research_paper_data, author_ids)
        return ResponseSchema(detail=f"Research paper {research_paper.id} created successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error creating research paper: {str(e)}", result=None)



@router.get("/all_with_authors")
async def get_all_research_papers_with_authors():
    try:
        research_papers = await ResearchService.get_all_with_authors()
        if research_papers is None:
            return []
        return research_papers
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting research papers: {str(e)}", result=None)


@router.get("/display-all")
async def get_all_papers_student_faculty(
    user_type: Optional[str] = None,
    type_paper: Optional[str] = Query(None, alias="type")
    ):
    try:
        research_papers = await ResearchPaperRepository.pagination_all_papers(user_type, type_paper)
        if research_papers is None:
            return []
        return research_papers
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting research papers: {str(e)}", result=None)


@router.get("/user", response_model=List[ResearchPaperResponse], response_model_exclude_none=True)
async def get_user_research_papers(
    type: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_papers_by_user(current_user, type)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        
        # Convert each ResearchPaper to ResearchPaperResponse
        response_papers = []
        for paper in research_papers:
            response_paper = ResearchPaperResponse(
                id=paper.id,
                title=paper.title,
                research_type=paper.research_type,
                submitted_date=str(paper.submitted_date),
                status=paper.status,
                file_path=paper.file_path,
                research_adviser=paper.research_adviser,
            )
            response_papers.append(response_paper)

        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)




@router.get("/{research_paper_id}",)
async def get_research_paper_with_authors(
        research_paper_id: str = Path(..., alias="research_paper_id"),
):
    '''
    This part kasi more on di ko na alam paano ko i-coconnect tong mga table pero try nyo nalang na didisplay naman na din data
    '''
    try:
        research_paper = await ResearchService.get_research_paper_with_authors(research_paper_id)
        return research_paper
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting research paper: {str(e)}", result=None)


@router.get("/paper-author-list/{research_paper_id}",)
async def show_paper_author_list(
        research_paper_id: str = Path(..., alias="research_paper_id"),
):
    '''
    This part kasi more on di ko na alam paano ko i-coconnect tong mga table pero try nyo nalang na didisplay naman na din data
    '''
    try:
        research_paper = await ResearchService.show_paper_author_list(research_paper_id)
        return research_paper
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting research paper: {str(e)}", result=None)






@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_research(
        research_id: str = Path(..., alias="id"),
):
    try:
        await ResearchPaperRepository.delete(research_id, db)  # pass Session instance to delete method
        return ResponseSchema(detail="Successfully deleted data !")
    except Exception as e:
        return ResponseSchema(detail=f"Error deleting research paper: {str(e)}", result=None)
   


@router.put("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def edit_research_paper(
   research_paper_id: str = Path(..., alias="id"),
   research_paper_data: ResearchEdit = Body(..., exclude=["status"])
):
   try:
       existing_research_paper = await ResearchService.get_research_paper(db, research_paper_id)

       if existing_research_paper is None:
           raise HTTPException(status_code=404, detail="Research paper not found")

       await ResearchService.update_research_paper(db, existing_research_paper, research_paper_data.dict(exclude={"id"}))

       return ResponseSchema(detail=f"Research paper {research_paper_id} updated successfully", result=None)
   except Exception as e:
       return ResponseSchema(detail=f"Error updating research paper: {str(e)}", result=None)
   



@router.get("/", response_model=List[ResearchPaperResponse])
async def get_all_research_papers():
    """
    Get all research papers from the database.
    """
    try:
        research_papers = await ResearchService.get_all_research_papers(db)
        
        # Convert the list of ResearchPaper to a list of ResearchPaperResponse
        response_papers = [
            ResearchPaperResponse(
                id=paper.id,
                title=paper.title,
                research_type=paper.research_type,
                submitted_date=str(paper.submitted_date),
                status = paper.status,
                file_path=paper.file_path,
                research_adviser=paper.research_adviser,
            )
            for paper in research_papers
        ]

        return response_papers
    except Exception as e:
       return ResponseSchema(detail=f"Error getting all research paper: {str(e)}", result=None)

@router.get("/{workflowstep_id}/{research_id}",)
async def get_research_paper_by_step_and_id(workflowstep_id: str,research_id: str):
    """
    Get ethics with workflowstep id and research that are connected
    """
    try:
        research_result = await WorkflowService.get_research_paper_by_step_and_id(workflowstep_id,research_id)
        return research_result
    except Exception as e:
        return ResponseSchema(detail=f"Error getting ethics related to paper: {str(e)}", result=None)

