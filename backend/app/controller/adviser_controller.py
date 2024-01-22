from typing import List, Optional, Union
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import AssignUserProfile, CopyRightWithResearchResponse, EthicsResponse, EthicsWithResearchResponse, FPSTest, FacultyResearchPaperCreate, FacultyResearchPaperUpdate, FullManuscriptWithResearchResponse, MakeExtension, ResearchPaperResponse, ResponseSchema, StatusUpdate
from app.service.research_service import ResearchService
from app.config import db
from app.service.assignTo_service import AssignToSection
from app.service.users_service import UserService
from app.model.research_paper import FacultyResearchPaper
from app.repository.users import UsersRepository
from app.repository.research_repo import ResearchPaperRepository

router = APIRouter(
    prefix="/faculty",
    tags=['Faculty Power'],
    dependencies=[Depends(JWTBearer())]
)

# ========================== POWER NG FACULTY =================

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
            "assignments": [],  # Initialize as an empty list
        }

        for assign in assignments:
            assign_details = {
                "research_type_name": assign["research_type_name"],
                "assignsection": [],
            }

            for section in assign["assignsection"]:
                assign_details["assignsection"].append({
                    "class_id": section["class_id"],
                    "course": section["course"],
                    "section": section["section"],
                })

            response_data["assignments"].append(assign_details)

        return AssignUserProfile(**response_data)

    except HTTPException as http_exc:
        raise http_exc  # Re-raise FastAPI HTTP exceptions

    except Exception as e:
        print(f"Internal Server Error: {e}")  # Print error details
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/adviser/{course}/{year}",)
async def get_user_research_papers(
    research_type: str,
    course: str,
    year: str,
    
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''
        ADVISER lang talaga
    '''
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_papers_by_adviser(db, research_type, current_user, course, year)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "research_type": paper.research_type,
                "status": paper.status
            }
            for paper in research_papers
        ]

        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)
    
@router.get("/adviser/defense/{course}/{year}",)
async def get_user_research_papers(
    defense_type: str,
    research_type: str,
    course: str,
    year: str,
    
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''
        ADVISER lang talaga
    '''
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_defense_by_adviser(db, research_type, current_user, course, year, defense_type)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "time": paper.time,
                "date": paper.date
            }
            for paper in research_papers
        ]

        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)


@router.get("/adviser/ethics/{course}/{year}")
async def get_adviser_research_papers_and_ethics(
    research_type: str,
    course: str,
    year: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''
        ADVISER lang talaga
    '''
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_ethics_by_adviser(db, research_type, current_user, course, year)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Ethics not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "status": paper.status
            }
            for paper in research_papers
        ]
        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user ethics papers: {str(e)}", result=None)
    

@router.get("/adviser/manuscript/{course}/{year}")
async def get_user_research_manuscripts(
    research_type: str,
    course: str,
    year: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''
        ADVISER lang talaga
    '''
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_manuscript_by_adviser(db, research_type, current_user, course, year)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "status": paper.status
            }
            for paper in research_papers
        ]
        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)



@router.get("/adviser/copyright/{course}/{year}")
async def get_faculty_copyright_info(
    research_type: str,
    course: str,
    year: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    '''
        ADVISER lang talaga
    '''
    
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        research_papers = await ResearchService.get_research_copyright_by_adviser(db, research_type, current_user, course, year)
        
        if research_papers is None:
            raise HTTPException(status_code=404, detail="Research paper not found")
        response_papers = [
            {
                "id": paper.id,
                "title": paper.title,
                "status": paper.status
            }
            for paper in research_papers
        ]
        return response_papers
    except Exception as e:
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)
    
    
    # ==============================================  APPROVING SECTIONSSS ===================================================================
    ##########################################################################################################################################


@router.put("/update_status/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    research_paper_id: str,
    status_update: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id'] 

    user_roles = await UsersRepository.get_user_roles(current_user)
    if "faculty" not in user_roles:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper.")
    
    try:
        research_paper = await ResearchService.update_research_paper_status(db, research_paper_id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)




@router.put("/approve_ethics/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    id: str,
    status_update: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']  # this line will show what role the logged-in user is

    user_roles = await UsersRepository.get_user_roles(current_user)
    if "faculty" not in user_roles:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper.")

    try:
        research_paper = await ResearchService.update_ethics_status(db, id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)
    

@router.put("/approve_manuscript/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    id: str,
    status_update: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']  # this line will show what role the logged-in user is

    user_roles = await UsersRepository.get_user_roles(current_user)
    if "faculty" not in user_roles:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper.")

    try:
        research_paper = await ResearchService.update_manuscript_status(db, id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)

@router.put("/approve_copyright/{id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    id: str,
    status_update: StatusUpdate,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']  # this line will show what role the logged-in user is

    user_roles = await UsersRepository.get_user_roles(current_user)
    if "faculty" not in user_roles:
        raise HTTPException(status_code=403, detail=f"You are not allowed to update the status of this research paper.")

    try:
        research_paper = await ResearchService.update_copyright_status(db, id, status_update.status)
        return ResponseSchema(detail=f"Research paper {research_paper.id} status updated successfully", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating research paper status: {str(e)}", result=None)
    

@router.put("/make-extension/{research_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper_status(
    id: str,
    make_extension: MakeExtension,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    # Extract the user role from the JWT token
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']  # this line will show what role the logged-in user is

    user_roles = await UsersRepository.get_user_roles(current_user)
    if "faculty" not in user_roles:
        raise HTTPException(status_code=403, detail=f"You are not allowed to use this feature")

    try:
        research_paper = await ResearchPaperRepository.make_paper_extension(db, id, make_extension)
        return ResponseSchema(detail=f"Research paper {research_paper.id} is now part of extension", result=research_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error making research extension: {str(e)}", result=None)
    
    
    
    
    
# todo make a api route for showing list of faculty and section and course they are adviser



# todo 
# ======================================= FAULTY UPLOAD OF PAPERS

#progress making research repo for faculty

# @router.post("/fps/upload-all")
# async def testing_fps(research_paper_data: List[FPSTest]):

#     try:
#         faculty_papers = await ResearchService.upload_multiple_faculty_papers(research_paper_data)
#         return ResponseSchema(detail="All research papers created successfully", result=[faculty_paper.dict() for faculty_paper in faculty_papers])
#     except ValueError as ve:
#         return ResponseSchema(detail=f"Error creating research paper: Invalid date format. Please use 'dd-mm-yyyy'.", result=None)
#     except HTTPException as e:
#         return ResponseSchema(detail=f"Error creating research paper: {str(e)}", result=None)



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
    except ValueError as ve:
        return ResponseSchema(detail=f"Error creating research paper: Invalid date format. Please use 'dd-mm-yyyy'.", result=None)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error creating research paper: {str(e)}", result=None)
    

    
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
    
    
    
def list_categories():
    return ["CHED Recognized", "Scopus", "Peer Reviewed", "Web Science"]
@router.get("/category_list",)
async def get_list_categories():
    """
    Get all user in USER TABLE
    """
    category = list_categories()
    return {"categories": category}


def list_publisher():
    return ["PUP Research Publication Office"]
@router.get("/publisher_list",)
async def get_list_publisher():
    """
    Get all user in USER TABLE
    """
    pub = list_categories()
    return {"publishers": pub}
