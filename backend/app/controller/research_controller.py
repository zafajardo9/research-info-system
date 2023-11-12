
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.service.research_service import ResearchService
from app.model.research_paper import ResearchPaper
from app.schema import ResearchPaperCreate, ResearchPaperResponse, ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.service.users_service import UserService
from datetime import datetime

from app.config import db
from app.repository.research_repo import ResearchPaperRepository

router = APIRouter(
    prefix="/research",
    tags=['Research'],
    dependencies=[Depends(JWTBearer())]
)


@router.post("/upload", response_model=ResponseSchema, response_model_exclude_none=True)
async def upload_research_paper(
    research_paper_data: ResearchPaperCreate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    username = token['username']

    # Get user_id by username
    user_id = await UserService.get_student_profile(username)

    # Link the research paper with the current user
    research_paper_data.author_id = user_id

    # Set submitted_date to the current date
    research_paper_data.submitted_date = datetime.now()

        # Create the research paper
    created_paper = await ResearchService.create_research_paper(db, research_paper_data, username)

    # Return a response with the detail field
    return ResponseSchema(detail=f"Research paper {created_paper.id} created successfully", result=created_paper)




# @router.get("/{research_paper_id}", response_model=ResearchPaperResponse)
# async def read_research_paper(research_paper_id: str):
#     get_paper = await ResearchService.get_research_paper(db, research_paper_id)
#     if get_paper is None:
#         raise HTTPException(status_code=404, detail="Research paper not found")
#     return get_paper


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


# @router.get("", response_model=ResponseSchema, response_model_exclude_none=True)
# async def get_all_person(
#         page: int = 1,
#         limit: int = 10,
#         columns: str = Query(None, alias="columns"),
#         sort: str = Query(None, alias="sort"),
#         filter: str = Query(None, alias="filter"),
# ):
#     result = await PersonRepository.get_all(page, limit, columns, sort, filter)
#     return ResponseSchema(detail="Successfully fetch person data by id !", result=result)
