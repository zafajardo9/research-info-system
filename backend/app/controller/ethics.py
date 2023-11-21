
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo

from app.config import db
from app.repository.research_repo import ResearchPaperRepository
from app.model import Users, Author, ResearchPaper
from app.service.users_service import UserService
from app.model.research_paper import Status
from app.schema import ResponseSchema

router = APIRouter(
    prefix="/ethics",
    tags=['Ethics'],
    dependencies=[Depends(JWTBearer())]
)


# @router.post("/upload", response_model=ResponseSchema, response_model_exclude_none=True)
# async def upload_research_paper(
#     research_paper_data: EthicsCreate,
#     research_id: str,
# ):
#     try:
#         research_paper = await ResearchService.create_research_paper(db, research_paper_data, research_id)
#         return ResponseSchema(detail=f"Research paper {research_paper.id} created successfully", result=research_paper)
#     except HTTPException as e:
#         return ResponseSchema(detail=f"Error creating research paper: {str(e)}", result=None)