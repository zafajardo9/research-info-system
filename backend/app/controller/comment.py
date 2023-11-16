from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session


from app.repository.auth_repo import JWTBearer, JWTRepo

from app.config import db
from app.schema import ResearchComment, ResearchCommentResponse, ResearchPaperCreate, ResponseSchema, ResearchPaper
from app.service.research_service import ResearchService
from app.repository.comment_repo import CommentRepository

router = APIRouter(
    prefix="/comments",
    tags=['Faculty Comments'],
    dependencies=[Depends(JWTBearer())]
)



@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def post_comment(
    faculty_comment: ResearchComment,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    """ So dito gagawin nya is nag rerely sa token. Kuninang current id ng nakalogin tapos need lang mag supply nung research paper id """
    token = JWTRepo.extract_token(credentials)
    current_user_id = token['user_id']

    try:
        comment = await ResearchService.post_comment(db, current_user_id, faculty_comment.research_id, faculty_comment.text)
        return ResponseSchema(detail=f"Comment {comment.id} created successfully", result=comment)
    except Exception as e:
        return ResponseSchema(detail=f"Error creating comment: {str(e)}", result=None)

#====================DISPLAY RELATED
@router.get("/{research_paper_id}", response_model=List[ResearchCommentResponse], response_model_exclude_none=True)
async def get_comments_by_research_id(
        research_paper_id: str = Path(..., alias="research_paper_id"),
):
    try:
        comments = await CommentRepository.get_comments_by_research_id(research_paper_id)
        return comments
    except Exception as e:
        return ResponseSchema(detail=f"Error getting comments: {str(e)}", result=None)


#=====================DELETE
@router.delete("/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_research(
        comment_id: str = Path(..., alias="id"),
):
    try:
        await CommentRepository.delete(comment_id)
        return ResponseSchema(detail=f"Successfully deleted comment {comment_id}!", result=comment_id)
    except Exception as e:
        return ResponseSchema(detail=f"Error deleting comment: {str(e)}", result=None)

