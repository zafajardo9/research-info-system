from typing import List
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security

from app.schema import ResponseSchema
from app.config import db
from app.service.all_about_info_service import AllInformationService
from app.repository.users import UsersRepository

router = APIRouter(
    prefix="/info",
    tags=['All Information For analytics'],
    dependencies=[Depends(JWTBearer())]
)


#FOR ADMIN

@router.get("/faculty/dashboard-faculty/")
async def read_student_count(type: str):
    total_count_student = await AllInformationService.get_student_count_all(db)
    total_count_prof = await AllInformationService.get_prof_count_all(db)
    total_count_adviser = await AllInformationService.get_adviser_count_all(db, type)
    
    
    proposal_count = await AllInformationService.count_proposal(db, type)
    proposal_rejected = await AllInformationService.proposal_rejected(db, type)
    ethics_approved = await AllInformationService.approved_ethics(db, type)
    ethics_revision = await AllInformationService.revision_ethics(db, type)
    
    copyright_approved = await AllInformationService.approved_copyright(db, type)
    copyright_revision = await AllInformationService.revision_copyright(db, type)
    
    manu_approved = await AllInformationService.approved_manuscript(db, type)
    manu_revision = await AllInformationService.revision_manuscript(db, type)

    
    result = [
        {
            "Students": total_count_student
        },
        
        {
            "Research Adviser": total_count_adviser
        },
        
        {
            "Research Professor": total_count_prof
        },
        
        {
            "Approved Proposal": proposal_count,
            "For Revision Proposal": proposal_rejected
        },
        
        {
            "Approved Ethics": ethics_approved,
            "For Revision Ethics": ethics_revision
        },
                
        {
            "Approved Copyright": copyright_approved,
            "For Revision Copyright": copyright_revision
        },
        {
            "Approved Full Manuscript": manu_approved,
            "For Revision Full Manuscript": manu_revision
        }
        
        ]
    return result


#number ng mga naka assign na prof per research type


@router.get("/admin/dashboard-admin/")
async def admin_info():
    pass


@router.get("/admin/count-research-info/all")
async def read_research_count_all():
    research_count = await AllInformationService.get_number_of_research_proposal(db)
    ethics_counts = await AllInformationService.get_number_ethics(db)
    manuscript_count = await AllInformationService.get_number_manuscript(db)
    copyright_count = await AllInformationService.get_number_copyright(db)
    return {
        "Research Count": research_count,
        "Ethics Count": ethics_counts,
        "Manuscript Count": manuscript_count,
        "Copyright Count": copyright_count,
        }




#FOR RESEARCH ADVISER ================= INFOR ABOUT THE RESEARCH  papers they are under to
@router.get("/research-adviser/number-of-advisory-by-status/{status}")
async def get_number_of_advisory_by_status(
    status: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''
    As a research adviser
    '''
    
    try: 
        token = JWTRepo.extract_token(credentials)
        current_user = token['user_id']
        count = await AllInformationService.get_number_of_advisory_by_status(db, current_user, status)
        
        ## dagdagan to base sa status dapat
        return {"Status": status, "Count" : count}
    except Exception as e:
        return ResponseSchema(detail=f"You have no number of research paper as an adviser: {str(e)}", result=None)

@router.get("/research-adviser/number-of-advisory-by-status")
async def get_number_of_advisory_by_status(
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
):
    '''FOR RESEARCH ADVISER
    Shows data about research paper under'''
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']
    total_number = await AllInformationService.get_number_of_my_advisory(db, current_user)
    ethics_count = await AllInformationService.get_number_of_ethics_by_adviser(db, current_user)
    copyright_count = await AllInformationService.get_number_of_copyright_by_adviser(db, current_user)
    manuscript_count = await AllInformationService.get_number_of_full_manuscript_by_adviser(db, current_user)
    
    
    proposal_status_count = await AllInformationService.get_status_count_of_proposal_by_adviser(db, current_user)
    ethics_status_count = await AllInformationService.get_status_count_of_ethics_by_adviser(db, current_user)
    copyright_status_count = await AllInformationService.get_status_count_of_copyright_by_adviser(db, current_user)
    manuscript_status_count = await AllInformationService.get_status_count_of_full_manuscript_by_adviser(db, current_user)
    return {
        "Number of my advisory": total_number,
        "PROPOSALS": {
            "Proposal Status Counts": proposal_status_count,
        },
        "ETHICS": {
            "COUNT OF SUBMITTED" : ethics_count,
            "Ethics Status Counts": ethics_status_count,
        },
        
        "COPYRIGHT": {
            "COUNT OF SUBMITTED": copyright_count,
            "Copyright Status Counts": copyright_status_count,
        },
        "FULL MANUSCRIPT": {
            "COUNT OF SUBMITTED": manuscript_count,
            "Manuscript Status Counts": manuscript_status_count,
        }
    }