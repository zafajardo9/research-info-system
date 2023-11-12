from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.service.research_service import ResearchService
from app.model.research_paper import ResearchPaper
from app.schema import ResearchPaperCreate, ResearchPaperResponse, ResponseSchema
from app.repository.auth_repo import JWTBearer, JWTRepo
from app.service.users_service import UserService
from datetime import datetime

from app.config import db

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