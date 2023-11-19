
from typing import List
from sqlalchemy.sql import select
from uuid import uuid4
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.service.research_service import ResearchService
from app.schema import AuthorResponse, AuthorSchema, CurrentUserResearchPaperResponse, ResearchEdit, ResearchPaperCreate, ResearchPaperResponse, ResearchPaperResponseOnly, ResponseSchema, StatusUpdate
from app.repository.auth_repo import JWTBearer, JWTRepo
from datetime import datetime

from app.config import db
from app.repository.research_repo import ResearchPaperRepository
from app.model import Users, Author, ResearchPaper
from app.service.users_service import UserService
from app.model.research_paper import Status

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



@router.get("/{research_paper_id}", response_model=ResearchPaperResponse)
async def read_research_paper(research_paper_id: str):

    try:
        get_paper = await ResearchService.get_research_paper(db, research_paper_id)
        if get_paper is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        
        # Convert ResearchPaper to ResearchPaperResponse
        response_paper = ResearchPaperResponse(
            id=get_paper.id,
            title=get_paper.title,
            content=get_paper.content,
            abstract=get_paper.abstract,
            research_type=get_paper.research_type,
            submitted_date=str(get_paper.submitted_date),
            status=get_paper.status,
            keywords=get_paper.keywords,
            file_path=get_paper.file_path,
            research_adviser=get_paper.research_adviser,
        )

        return response_paper
    except Exception as e:
        return ResponseSchema(detail=f"Error reading or getting research paper: {str(e)}", result=None)

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
   research_paper_data: ResearchEdit = Body(...)
):
   try:
       # Fetch the existing research paper
       existing_research_paper = await ResearchService.get_research_paper(db, research_paper_id)

       if existing_research_paper is None:
           raise HTTPException(status_code=404, detail="Research paper not found")

       # Update the research paper
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
                content=paper.content,
                abstract=paper.abstract,
                research_type=paper.research_type,
                submitted_date=str(paper.submitted_date),
                status = paper.status,
                keywords=paper.keywords,
                file_path=paper.file_path,
                research_adviser=paper.research_adviser,
            )
            for paper in research_papers
        ]

        return response_papers
    except Exception as e:
       return ResponseSchema(detail=f"Error getting all research paper: {str(e)}", result=None)



@router.get("/current_user_research_paper", response_model=List[ResearchPaperResponseOnly])
async def get_current_user_research_paper(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    """ Get the research paper related to the logged-in user #NOT WORKING """
    try:
        token = JWTRepo.extract_token(credentials)
        current_user_id = token['user_id']

        research_papers_with_authors = await ResearchService.get_research_papers_by_user_id(db, current_user_id)

        if not research_papers_with_authors:
            # Handle empty list case
            return []

        response_papers = []
        for paper in research_papers_with_authors:
            # Check if any field is None and replace it with default values
            response_papers.append(
                ResearchPaperResponseOnly(
                    id=paper.id,
                    title=paper.title or "",
                    content=paper.content or "",
                    abstract=paper.abstract or "",
                    research_type=paper.research_type or "",
                    submitted_date=str(paper.submitted_date),
                    status=paper.status,
                    keywords=paper.keywords or "",
                    file_path=paper.file_path or "",
                    research_adviser=paper.research_adviser or "",
                    authors=[AuthorResponse.from_orm(author).__dict__ for author in paper.authors]
                )
            )

        return response_papers

    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting research papers: {str(e.detail)}", result=None)

# ========================== POWER NG FACULTY =================

@router.put("/update_status/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    research_paper_id: str,
    status_update: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user_role = token['role'] #this line will show what role the logged in user is

    is_allowed = await ResearchService.check_faculty_permission(research_paper_id, current_user_role)
    if not is_allowed:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper. Your role is {current_user_role}.")
    # Update the status
    try:
        research_paper = await ResearchService.update_research_paper_status(db, research_paper_id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)