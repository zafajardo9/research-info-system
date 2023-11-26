from typing import List, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import CopyRightWithResearchResponse, EthicsResponse, EthicsWithResearchResponse, FullManuscriptWithResearchResponse, ResearchPaperResponse, ResponseSchema, StatusUpdate
from app.service.research_service import ResearchService
from app.config import db

router = APIRouter(
    prefix="/faculty",
    tags=['Faculty Power'],
    dependencies=[Depends(JWTBearer())]
)

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

    is_allowed = await ResearchService.check_faculty_permission(current_user_role)
    if not is_allowed:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper. Your role is {current_user_role}.")
    # Update the status
    try:
        research_paper = await ResearchService.update_research_paper_status(db, research_paper_id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)



@router.get("/adviser", response_model=List[ResearchPaperResponse], response_model_exclude_none=True)
async def get_user_research_papers(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''
        Faculty lang para malaman nila yung mga research paper na adviser sila
    '''
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_papers_by_adviser(db, current_user)
        
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
    

@router.get("/adviser/ethics", response_model=List[EthicsWithResearchResponse], response_model_exclude_none=True)
async def get_adviser_research_papers_and_ethics(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer()),
):
    """
    Retrieve a list of research papers under the current adviser along with associated ethics.
    """

    # Extract user_id from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user_id = token['user_id']

    try:
        research_papers = await ResearchService.get_research_ethics_by_adviser(db, current_user_id)
        
        if research_papers is None:
            return [{"Ethic": "No list of ethics found under you"}]  # Return a list with a single item
        
        # Convert each ResearchPaper to ResearchPaperResponse
        response_papers = []
        for research_paper, ethics in research_papers:
            response_paper = EthicsWithResearchResponse(
                id=ethics.id,
                modified_at=ethics.modified_at,
                created_at=ethics.created_at,
                letter_of_intent=ethics.letter_of_intent,
                urec_9=ethics.urec_9,
                urec_10=ethics.urec_10,
                urec_11=ethics.urec_11,
                urec_12=ethics.urec_12,
                certificate_of_validation=ethics.certificate_of_validation,
                co_authorship=ethics.co_authorship,
                research_paper_id=ethics.research_paper_id,
                status=ethics.status,
                title=research_paper.title,
            )
            response_papers.append(response_paper)

        return response_papers
    except Exception as e:
        return [{"Error": f"Error getting user research papers: {str(e)}"}]
    
@router.get("/adviser/manuscript", response_model=List[FullManuscriptWithResearchResponse], response_model_exclude_none=True)
async def get_user_research_papers(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''
        Faculty lang para malaman nila yung mga research paper na adviser sila
    '''
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_manuscript_by_adviser(db, current_user)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        
        # Convert each ResearchPaper to ResearchPaperResponse
        response_papers = []
        for research_paper, manuscript in research_papers:
            response_paper = FullManuscriptWithResearchResponse(
                id = manuscript.id,
                modified_at = manuscript.modified_at,
                created_at = manuscript.created_at,
                research_paper_id = manuscript.research_paper_id,
                content = manuscript.content,
                keywords = manuscript.keywords,
                abstract = manuscript.abstract,
                file = manuscript.file,
                status = manuscript.status,
                title = research_paper.title

            )
            response_papers.append(response_paper)

        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)

@router.get("/adviser/copyright", response_model=List[CopyRightWithResearchResponse], response_model_exclude_none=True)
async def get_user_research_papers(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''
        Faculty lang para malaman nila yung mga research paper na adviser sila
    '''
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_manuscript_by_adviser(db, current_user)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        
        # Convert each ResearchPaper to ResearchPaperResponse
        response_papers = []
        for research_paper, copyright in research_papers:
            response_paper = CopyRightWithResearchResponse(
                id=copyright.id,
                modified_at=copyright.modified_at,
                created_at=copyright.created_at,
                research_paper_id=copyright.research_paper_id,
                co_authorship=copyright.co_authorship,
                affidavit_co_ownership=copyright.affidavit_co_ownership,
                joint_authorship=copyright.joint_authorship,
                approval_sheet=copyright.approval_sheet,
                receipt_payment=copyright.receipt_payment,
                recordal_slip=copyright.recordal_slip,
                acknowledgement_receipt=copyright.acknowledgement_receipt,
                certificate_copyright=copyright.certificate_copyright,
                recordal_template=copyright.recordal_template,
                ureb_18=copyright.ureb_18,
                journal_publication=copyright.journal_publication,
                copyright_manuscript=copyright.copyright_manuscript,
                status=copyright.status,
                title=research_paper.title
            )
            response_papers.append(response_paper)

        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)

@router.put("/approve_ethics/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    research_paper_id: str,
    status_update: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user_role = token['role'] #this line will show what role the logged in user is

    is_allowed = await ResearchService.check_faculty_permission(current_user_role)
    if not is_allowed:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper. Your role is {current_user_role}.")
    # Update the status
    try:
        research_paper = await ResearchService.update_research_paper_status(db, research_paper_id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)
    

@router.put("/approve_manuscript/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    research_paper_id: str,
    status_update: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user_role = token['role'] #this line will show what role the logged in user is

    is_allowed = await ResearchService.check_faculty_permission(current_user_role)
    if not is_allowed:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper. Your role is {current_user_role}.")
    # Update the status
    try:
        research_paper = await ResearchService.update_manuscript_status(db, research_paper_id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)

@router.put("/approve_copyright/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    research_paper_id: str,
    status_update: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user_role = token['role'] #this line will show what role the logged in user is

    is_allowed = await ResearchService.check_faculty_permission(current_user_role)
    if not is_allowed:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper. Your role is {current_user_role}.")
    # Update the status
    try:
        research_paper = await ResearchService.update_copyright_status(db, research_paper_id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)