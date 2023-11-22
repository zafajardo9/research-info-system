
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo

from app.config import db
from app.schema import EthicsCreate, EthicsResponse, ResponseSchema
from app.service.ethics_service import EthicsService

router = APIRouter(
    prefix="/ethics",
    tags=['Ethics'],
    dependencies=[Depends(JWTBearer())]
)


@router.post("/upload", response_model=ResponseSchema, response_model_exclude_none=True)
async def upload_ethics(
    ethics_data: EthicsCreate,
    research_paper_id: str,
):
    try:
        # Call the service method to upload ethics data
        ethics_paper = await EthicsService.upload_ethics(db, ethics_data, research_paper_id)
        
        # Return the response with the created research paper ID
        return ResponseSchema(detail=f"Ethics data for research paper uploaded successfully", result=ethics_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error uploading ethics data: {str(e)}", result=None)




@router.get("/get_ethics_by_research/{research_paper_id}", response_model=EthicsResponse)
async def get_ethics_by_research_paper_id(research_paper_id: str):
    try:
        ethics_data = await EthicsService.get_ethics_by_research_paper_id(db, research_paper_id)
        if ethics_data is None:
            raise HTTPException(status_code=404, detail="No Ethics Found")
        
        response_ethics = EthicsResponse(
            id=ethics_data.id,
            created_at = ethics_data.created_at,
            letter_of_intent=ethics_data.letter_of_intent,
            urec_9=ethics_data.urec_9,
            urec_10=ethics_data.urec_10,
            urec_11=ethics_data.urec_11,
            urec_12=ethics_data.urec_12,
            co_authorship = ethics_data.co_authorship,
            certificate_of_validation=ethics_data.certificate_of_validation,
            research_paper_id=ethics_data.research_paper_id,
        )

        return response_ethics

    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)

    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error retrieving ethics data: {str(e)}")
        return ResponseSchema(detail=f"Error retrieving ethics data: {str(e)}", result=None)





@router.put("/update/{ethics_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_ethics(
    ethics_data: EthicsCreate,
    ethics_id: str,
):
    '''
    NOT WORKING PA
    '''
    try:
        # Call the service method to update ethics data by research paper ID
        updated_ethics = await EthicsService.update_ethics(db, ethics_data, ethics_id)
        
        # Return the response with the updated ethics data
        return ResponseSchema(detail=f"Ethics data for research paper {ethics_id} updated successfully", result=updated_ethics)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error updating ethics data: {str(e)}", result=None)
    



@router.delete("/delete_ethics/{ethics_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_ethics(ethics_id: str):
    '''
    Delete only nung ethics
    '''
    try:
        # Call the service method to delete ethics data by research paper ID
        await EthicsService.delete_ethics(db, ethics_id)
        
        # Return the response with a success message
        return ResponseSchema(detail=f"Ethics data for research paper {ethics_id} deleted successfully", result=None)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error deleting ethics data: {str(e)}", result=None)