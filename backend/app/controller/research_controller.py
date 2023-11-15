
from typing import List
from uuid import uuid4
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.service.research_service import ResearchService
from app.schema import ResearchEdit, ResearchPaperCreate, ResearchPaperResponse, ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from datetime import datetime

from app.config import db
from app.repository.research_repo import ResearchPaperRepository
from app.model import Users, Author, ResearchPaper
from app.service.users_service import UserService

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
    except Exception as e:
        return ResponseSchema(detail=f"Error creating research paper: {str(e)}", result=None)




@router.get("/{research_paper_id}", response_model=ResearchPaperResponse)
async def read_research_paper(research_paper_id: str):
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
        keywords=get_paper.keywords,
        file_path=get_paper.file_path,
        research_adviser=get_paper.research_adviser,
    )

    return response_paper

@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_research(
        research_id: str = Path(..., alias="id"),
):
    await ResearchPaperRepository.delete(research_id)
    return ResponseSchema(detail="Successfully deleted data !")


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
            keywords=paper.keywords,
            file_path=paper.file_path,
            research_adviser=paper.research_adviser,
        )
        for paper in research_papers
    ]

    return response_papers

