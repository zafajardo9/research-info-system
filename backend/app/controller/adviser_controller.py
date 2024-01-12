from typing import List, Optional, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import AssignUserProfile, CopyRightWithResearchResponse, EthicsResponse, EthicsWithResearchResponse, FacultyResearchPaperCreate, FacultyResearchPaperUpdate, FullManuscriptWithResearchResponse, ResearchPaperResponse, ResponseSchema, StatusUpdate
from app.service.research_service import ResearchService
from app.config import db
from app.service.assignTo_service import AssignToSection
from app.service.users_service import UserService
from app.model.research_paper import FacultyResearchPaper

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



@router.get("/my-assigned-research-section", response_model=AssignUserProfile)
async def read_user_assignments(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    try:
        user_profile = await UserService.get_faculty_profile_by_ID(current_user)
        if user_profile is None:
            raise HTTPException(status_code=404, detail="User profile not found")

        assignments = await AssignToSection.display_assignments_by_user(user_profile["id"])
        if assignments is None:
            raise HTTPException(status_code=404, detail="Assignments not found")

        response_data = {
            "user_profile": user_profile,
            "assignments": assignments.dict(),
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
async def get_user_research_manuscripts(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        result = await ResearchService.get_research_manuscript_by_adviser(db, current_user)

        # Convert each result row to a response model
        response_papers = []
        for research_paper, manuscript in result:
            response_paper = FullManuscriptWithResearchResponse(
                id=manuscript.id,
                modified_at=manuscript.modified_at,
                created_at=manuscript.created_at,
                research_paper_id=manuscript.research_paper_id,
                content=manuscript.content,
                keywords=manuscript.keywords,
                abstract=manuscript.abstract,
                file=manuscript.file,
                status=manuscript.status,
                title=research_paper.title,
            )
            response_papers.append(response_paper)

        # Return the list of response papers
        return response_papers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user research manuscripts: {str(e)}")


@router.get("/adviser/copyright", response_model=List[CopyRightWithResearchResponse], response_model_exclude_none=True)
async def get_faculty_copyright_info(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        result = await ResearchService.get_research_copyright_by_adviser(db, current_user)

        # Convert each result row to a response model
        response_copyrights = []
        for research_paper, copyright_info in result:
            response_copyright = CopyRightWithResearchResponse(
                id=copyright_info.id,
                modified_at=copyright_info.modified_at,
                created_at=copyright_info.created_at,
                research_paper_id=copyright_info.research_paper_id,
                co_authorship=copyright_info.co_authorship,
                affidavit_co_ownership=copyright_info.affidavit_co_ownership,
                joint_authorship=copyright_info.joint_authorship,
                approval_sheet=copyright_info.approval_sheet,
                receipt_payment=copyright_info.receipt_payment,
                recordal_slip=copyright_info.recordal_slip,
                acknowledgement_receipt=copyright_info.acknowledgement_receipt,
                certificate_copyright=copyright_info.certificate_copyright,
                recordal_template=copyright_info.recordal_template,
                ureb_18=copyright_info.ureb_18,
                journal_publication=copyright_info.journal_publication,
                copyright_manuscript=copyright_info.copyright_manuscript,
                status=copyright_info.status,
                title=research_paper.title,
            )
            response_copyrights.append(response_copyright)

        # Return the list of response copyrights
        return response_copyrights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting faculty copyright information: {str(e)}")

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
    
    
    
    
# todo make a api route for showing list of faculty and section and course they are adviser



# todo 
# ======================================= FAULTY UPLOAD OF PAPERS

#progress making research repo for faculty


@router.get("/faculty-papers/list")
async def get_faculty_research_papers():
    try:
        research_papers = await ResearchService.get_faculty_research_papers_with_user_info()
        if research_papers:
            return research_papers
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)


@router.post("/upload-my-papers")
async def upload_faculty_paper(
    research_paper_data: FacultyResearchPaperCreate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        faculty_paper = await ResearchService.upload_faculty_paper(current_user, research_paper_data)
        return ResponseSchema(detail=f"Research paper {faculty_paper.id} created successfully", result=faculty_paper.dict())
    except HTTPException as e:
        return ResponseSchema(detail=f"Error creating research paper: {str(e)}", result=None)
    
# @router.post("/upload-my-papers")
# async def upload_faculty_paper(
#     research_paper_data: FacultyResearchPaperCreate,
#     credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
#     token = JWTRepo.extract_token(credentials)
#     current_user = token['user_id']

#     try:
#         faculty_paper = await ResearchService.upload_faculty_paper(current_user, research_paper_data)
#         return ResponseSchema(detail=f"Research paper {faculty_paper.id} created successfully", result=faculty_paper.dict())
#     except HTTPException as e:
#         return ResponseSchema(detail=f"Error creating research paper: {str(e)}", result=None)
    
@router.get("/my-research-papers", response_model=Optional[List[FacultyResearchPaper]], response_model_exclude_none=True)
async def get_faculty_research_papers(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)
    current_user_id = token['user_id']

    try:
        research_papers = await ResearchService.get_faculty_research_papers(current_user_id)
        if research_papers:
            return research_papers
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)
    
    
@router.get("/my-research-papers/{research_paper_id}", response_model=Optional[FacultyResearchPaper], response_model_exclude_none=True)
async def get_faculty_research_papers(
    research_paper_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)

    try:
        research_papers = await ResearchService.get_faculty_research_papers_by_id(research_paper_id)
        if research_papers:
            return research_papers
        else:
            return None
    except HTTPException as e:
        return ResponseSchema(detail=f"Error retrieving research papers: {str(e)}", result=None)
    
    
@router.delete("/delete-my-research-papers/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_faculty_research_paper(
    research_paper_id: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):

    try:
        await ResearchService.delete_faculty_research_paper(research_paper_id)
        return ResponseSchema(detail=f"Research paper {research_paper_id} deleted successfully", result=None)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error deleting research paper: {str(e)}", result=None)
    
    
@router.put("/my-research-papers/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_faculty_research_paper(
    research_paper_id: str,
    research_paper_data: FacultyResearchPaperUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    token = JWTRepo.extract_token(credentials)

    try:
        await ResearchService.update_faculty_research_paper(research_paper_id, research_paper_data)
        return ResponseSchema(detail=f"Research paper {research_paper_id} updated successfully", result=None)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper: {str(e)}", result=None)