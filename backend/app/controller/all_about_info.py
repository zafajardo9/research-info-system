import logging
from typing import List, Optional
from app.service.research_service import ResearchService
from fastapi import APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from fastapi.responses import JSONResponse

from app.schema import ResponseSchema
from app.config import db
from app.service.all_about_info_service import AllInformationService
from app.repository.users import UsersRepository
from imagekitio import ImageKit


import pandas as pd
import aiofiles
import os
from uuid import uuid4
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



imagekit = ImageKit(
    private_key=os.getenv('IMAGEKIT_PRIVATE_KEY'),
    public_key=os.getenv('IMAGEKIT_PUBLIC_KEY'),
    url_endpoint=os.getenv('IMAGEKIT_URL_ENDPOINT')
)


router = APIRouter(
    prefix="/info",
    tags=['All Information For analytics'],
    dependencies=[Depends(JWTBearer())]
)


#FOR ADMIN

@router.get("/faculty/dashboard-faculty/")
async def read_student_count(
    type: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):
    try: 
        token = JWTRepo.extract_token(credentials)
        current_user = token['user_id']
        
        
        total_count_student = await AllInformationService.get_student_count_all(db)
        total_count_prof = await AllInformationService.get_prof_count_all(db)
        
        number_advisee = await AllInformationService.user_number_of_advisee(db, current_user, type)
        total_count_adviser = await AllInformationService.get_adviser_count_all(db, type)
        
        
        proposal_count = await AllInformationService.count_proposal(db, type, current_user)
        proposal_rejected = await AllInformationService.proposal_rejected(db, type, current_user)
        ethics_approved = await AllInformationService.approved_ethics(db, type, current_user)
        ethics_revision = await AllInformationService.revision_ethics(db, type, current_user)
        
        copyright_approved = await AllInformationService.approved_copyright(db, type, current_user)
        copyright_revision = await AllInformationService.revision_copyright(db, type, current_user)
        
        manu_approved = await AllInformationService.approved_manuscript(db, type, current_user)
        manu_revision = await AllInformationService.revision_manuscript(db, type, current_user)

        
        result = [
            {
                "Students": total_count_student,
                "Research Adviser": total_count_adviser,
                "Research Professor": total_count_prof
            },
            {
                "Advisee": number_advisee
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
    except Exception as e:
        return ResponseSchema(detail=f"You have no number of research paper as an adviser: {str(e)}", result=None)




@router.get("/print-all-info-student")
async def get_all_research_papers_with_authors(type: str, section:str):
    try:
        research_papers = await ResearchService.get_all_for_pdf(type, section)
        if research_papers is None:
            return []
        return research_papers
    
    except HTTPException as e:
        return ResponseSchema(detail=f"Error getting research papers: {str(e)}", result=None)





#number ng mga naka assign na prof per research type
@router.get("/admin/dashboard-admin/")
async def admin_info():
    
    return {
        "Total number across all courses" : await AllInformationService.total_number_of_papers(db),
        "BSIT" : await AllInformationService.number_of_papers_by_course(db, "BSIT"),
        "BBTLEDHE" : await AllInformationService.number_of_papers_by_course(db, "BBTLEDHE"),
        "BTLEDICT" : await AllInformationService.number_of_papers_by_course(db, "BTLEDICT"),
        "BSBAHRM": await AllInformationService.number_of_papers_by_course(db, "BSBAHRM"),
        "BSBA-MM": await AllInformationService.number_of_papers_by_course(db, "BSBA-MM"),
        "BSENTREP": await AllInformationService.number_of_papers_by_course(db, "BSENTREP"),
        "BPAPFM": await AllInformationService.number_of_papers_by_course(db, "BPAPFM"),
        "DOMTMOM": await AllInformationService.number_of_papers_by_course(db, "DOMTMOM"),
        #"metrics": await AllInformationService.compute_collaboration_metrics(db, "b3adcb3b-79cd-4862-8738-7f6e674548d2")
        "Faculty Copyrighted Papers Total": await AllInformationService.number_faculty_paper(db),
        }


@router.get("/admin/all-collaboration-metrics")
async def get_all_collaboration_metrics():
    all_metrics = await AllInformationService.compute_all_collaboration_metrics(db)
    return {"all_metrics": all_metrics}



@router.get("/admin/dashboard-2/")
async def admin_2(
    type: str,
    credentials: HTTPAuthorizationCredentials = Security(JWTBearer())
    ):
    try: 

        
        total_count_student = await AllInformationService.get_student_count_all(db)
        total_count_prof = await AllInformationService.get_prof_count_all(db)
        
        #number_advisee = await AllInformationService.user_number_of_advisee(db, current_user, type)
        total_count_adviser = await AllInformationService.get_adviser_count_all(db, type)
        
        
        proposal_count = await AllInformationService.overall_count_proposal(db, type)
        proposal_rejected = await AllInformationService.overall_proposal_rejected(db, type)
        ethics_approved = await AllInformationService.overall_approved_ethics(db, type)
        ethics_revision = await AllInformationService.overall_revision_ethics(db, type)
        
        copyright_approved = await AllInformationService.overall_approved_copyright(db, type)
        copyright_revision = await AllInformationService.overall_revision_copyright(db, type)
        
        manu_approved = await AllInformationService.overall_approved_manuscript(db, type)
        manu_revision = await AllInformationService.overall_revision_manuscript(db, type)

        
        result = [
            {
                "Students": total_count_student,
                "Research Adviser": total_count_adviser,
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
    except Exception as e:
        return ResponseSchema(detail=f"You have no number of research paper as an adviser: {str(e)}", result=None)



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
        return {"Status": status, "Count (Any research types)" : count}
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
    
@router.get("/print/print-all-research")
async def print_all_filed(type: str, section: Optional[str] = Query(None, alias="section")):
    try:


        # Fetch the research papers (this is a mock function, replace with your actual logic)
        research_papers = await ResearchService.get_all_for_pdf(type, section)
        print(research_papers)
        if research_papers is None:
            logging.warning("No research papers found")
            return []

        # Log research papers fetched
        logging.info(f"Research papers fetched: {research_papers}")

        # Convert the data to a DataFrame
        df = pd.DataFrame(research_papers)

        # Generate a unique filename
        file_id = uuid4().hex
        filename = f"Dashboard_research_{file_id}.xlsx"
        filepath = f"./{filename}"

        # Save the DataFrame to an Excel file
        df.to_excel(filepath, index=False)

        # Log file creation
        logging.info(f"Excel file created at {filepath}")

        # Upload the file to ImageKit
        with open(filepath, "rb") as file:
            upload_response = imagekit.upload_file(
                file=file,
                file_name=filename
            )

        # Remove the local file after upload
        os.remove(filepath)

        # Log file upload
        logging.info(f"File uploaded to ImageKit: {upload_response}")

        # Access the URL from the UploadFileResult object
        file_url = upload_response.url

        # Generate a URL with transformations
        image_url = imagekit.url({
            "src": file_url,
            "transformation": [{
                "height": "300",
                "width": "400",
                "raw": "ar-4-3,q-40"
            }]
        })

        # Return the transformed file link
        return {"file_link": image_url}
        
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ResponseSchema(detail=f"Error getting research papers: {str(e)}").dict()
        )