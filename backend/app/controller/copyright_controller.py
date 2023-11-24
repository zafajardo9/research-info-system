from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials

from app.config import db
from app.schema import CopyRightCreate, CopyRightUpdate, CopyRightResponse, ResponseSchema
from app.service.copyright_service import CopyrightService


router = APIRouter(
    prefix="/copyright",
    tags=['Copyright'],
    dependencies=[Depends(JWTBearer())]
)



@router.post("/upload", response_model=ResponseSchema, response_model_exclude_none=True)
async def upload_ethics(
    ethics_data: CopyRightCreate,
):
    try:
        # Call the service method to upload ethics data
        ethics_paper = await CopyrightService.upload_copyright(db, ethics_data)
        
        # Return the response with the created research paper ID
        return ResponseSchema(detail=f"Copyright data for research paper uploaded successfully", result=ethics_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error uploading copyright data: {str(e)}", result=None)


@router.get("/get_copyright_by_research/{research_paper_id}", response_model=CopyRightResponse)
async def get_ethics_by_research_paper_id(research_paper_id: str):
    try:
        copyright_data = await CopyrightService.get_copyright_by_research_paper_id(db, research_paper_id)
        if copyright_data is None:
            raise HTTPException(status_code=404, detail="No Manuscript Found")
        
        response_ethics = CopyRightResponse(
            id = copyright_data.id,
            created_at = copyright_data.created_at,
            research_paper_id = copyright_data.research_paper_id,
            co_authorship = copyright_data.co_authorship,
            affidavit_co_ownership = copyright_data.affidavit_co_ownership,
            joint_authorship = copyright_data.joint_authorship,
            approval_sheet = copyright_data.approval_sheet,
            receipt_payment = copyright_data.receipt_payment,
            recordal_slip = copyright_data.recordal_slip,
            acknowledgement_receipt = copyright_data.acknowledgement_receipt,
            certificate_copyright = copyright_data.certificate_copyright,
            recordal_template = copyright_data.recordal_template,
            ureb_18 = copyright_data.ureb_18,
            journal_publication = copyright_data.journal_publication,
            copyright_manuscript = copyright_data.copyright_manuscript,
        )

        return response_ethics

    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)

    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error retrieving manuscript data: {str(e)}")
        return ResponseSchema(detail=f"Error retrieving manuscript data: {str(e)}", result=None)

@router.put("/update/{copyright_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_ethics(
    copyright_data: CopyRightUpdate,
    copyright_id: str,
):
    try:
        # Call the service method to update ethics data by ethics ID
        updated_ethics = await CopyrightService.update_copyright(db, copyright_data, copyright_id)
        
        # Return the response with the updated ethics data
        return ResponseSchema(detail=f"Copyright data for research paper {copyright_id} updated successfully", result=updated_ethics)
    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)
    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error updating copyright data: {str(e)}")
        return ResponseSchema(detail=f"Error updating copyright data: {str(e)}", result=None)



@router.delete("/delete_copyright/{copyright_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_ethics(copyright_id: str):
    '''
    Delete only nung copyright
    '''
    try:
        # Call the service method to delete ethics data by research paper ID
        await CopyrightService.delete_copyright(db, copyright_id)
        
        # Return the response with a success message
        return ResponseSchema(detail=f"Copyright data for research paper {copyright_id} deleted successfully", result=None)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error deleting copyright data: {str(e)}", result=None)
    


@router.get("/user", response_model=CopyRightResponse, response_model_exclude_none=True)
async def get_user_research_paper(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        # Call the service method to get ethics data for the logged-in user
        copyright_data = await CopyrightService.get_manuscript_by_user(db, current_user)
        
        if copyright_data is None:
            raise HTTPException(status_code=404, detail="No Ethics Found for the logged-in user")

        # Create an EthicsResponse instance
        copyright_data = CopyRightResponse(
            id = copyright_data.id,
            created_at = copyright_data.created_at,
            research_paper_id = copyright_data.research_paper_id,
            co_authorship = copyright_data.co_authorship,
            affidavit_co_ownership = copyright_data.affidavit_co_ownership,
            joint_authorship = copyright_data.joint_authorship,
            approval_sheet = copyright_data.approval_sheet,
            receipt_payment = copyright_data.receipt_payment,
            recordal_slip = copyright_data.recordal_slip,
            acknowledgement_receipt = copyright_data.acknowledgement_receipt,
            certificate_copyright = copyright_data.certificate_copyright,
            recordal_template = copyright_data.recordal_template,
            ureb_18 = copyright_data.ureb_18,
            journal_publication = copyright_data.journal_publication,
            copyright_manuscript = copyright_data.copyright_manuscript,
        )

        return copyright_data

    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)

    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error getting user research papers: {str(e)}")
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)
