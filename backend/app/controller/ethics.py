
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo

from app.config import db
from app.schema import EthicsCreate, EthicsResponse, EthicsUpdate, ResponseSchema
from app.service.ethics_service import EthicsService
from app.service.workflow_service import WorkflowService
from app.repository.ethics_repo import EthicsRepository

router = APIRouter(
    prefix="/ethics",
    tags=['Ethics'],
    dependencies=[Depends(JWTBearer())]
)


@router.post("/upload", response_model=ResponseSchema, response_model_exclude_none=True)
async def upload_ethics(
    ethics_data: EthicsCreate,
):
    try:
        # Call the service method to upload ethics data
        ethics_paper = await EthicsService.upload_ethics(db, ethics_data)
        
        # Return the response with the created research paper ID
        return ResponseSchema(detail=f"Ethics data for research paper uploaded successfully", result=ethics_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error uploading ethics data: {str(e)}", result=None)



@router.get("/get-ethics/{id}",)
async def get_ethics_target(id: str):
    try:
        response = await EthicsRepository.get_ethics_by_id(db, id)
        if response is None:
            raise HTTPException(status_code=404, detail="No Manuscript Found")

        return response
    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)

    except Exception as e:
        print(f"Error retrieving manuscript data: {str(e)}")
        return ResponseSchema(detail=f"Error retrieving manuscript data: {str(e)}", result=None)



@router.get("/get_ethics_by_research/{research_paper_id}", response_model=EthicsResponse)
async def get_ethics_by_research_paper_id(research_paper_id: str):
    try:
        ethics_data = await EthicsService.get_ethics_by_research_paper_id(db, research_paper_id)
        if ethics_data is None:
            raise HTTPException(status_code=404, detail="No Ethics Found")
        
        response_ethics = EthicsResponse(
            id=ethics_data.id,
            workflow_step_id=ethics_data.workflow_step_id,
            modified_at = ethics_data.modified_at,
            created_at = ethics_data.created_at,
            letter_of_intent=ethics_data.letter_of_intent,
            urec_9=ethics_data.urec_9,
            urec_10=ethics_data.urec_10,
            urec_11=ethics_data.urec_11,
            urec_12=ethics_data.urec_12,
            co_authorship = ethics_data.co_authorship,
            certificate_of_validation=ethics_data.certificate_of_validation,
            research_paper_id=ethics_data.research_paper_id,
            status=ethics_data.status
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
    ethics_data: EthicsUpdate,
    ethics_id: str,
):
    try:
        # Call the service method to update ethics data by ethics ID
        updated_ethics = await EthicsService.update_ethics(db, ethics_data, ethics_id)
        
        # Return the response with the updated ethics data
        return ResponseSchema(detail=f"Ethics data for research paper {ethics_id} updated successfully", result=updated_ethics)
    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)
    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error updating ethics data: {str(e)}")
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
    


@router.get("/user", response_model=List[EthicsResponse])
async def get_user_research_paper(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        ethics_data_list = await EthicsService.get_ethics_by_user(db, current_user)
        
        response_ethics_list = []
        for ethics_data in ethics_data_list:
            response_ethics = EthicsResponse(
                id=ethics_data.id,
                created_at=ethics_data.created_at,
                modified_at=ethics_data.modified_at,
                letter_of_intent=ethics_data.letter_of_intent,
                urec_9=ethics_data.urec_9,
                urec_10=ethics_data.urec_10,
                urec_11=ethics_data.urec_11,
                urec_12=ethics_data.urec_12,
                certificate_of_validation=ethics_data.certificate_of_validation,
                co_authorship=ethics_data.co_authorship,
                status=ethics_data.status,
                research_paper_id=ethics_data.research_paper_id,
            )
            response_ethics_list.append(response_ethics)

        if not response_ethics_list:
            raise HTTPException(status_code=404, detail="No Ethics Found for the logged-in user")

        return response_ethics_list

    except HTTPException as e:
        if e.status_code == 404:
            return ResponseSchema(detail="No Ethics Found for the logged-in user", result=None)
        else:
            return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)

    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error getting user research papers: {str(e)}")
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)
    
    
@router.get("/{workflowstep_id}/{research_id}",)
async def get_ethics_by_workflow_step_id(workflowstep_id: str,research_id: str):
    """
    Get ethics with workflowstep id and research that are connected
    """
    try:
        ethics_result = await WorkflowService.get_ethics_by_workflow_step_id(workflowstep_id,research_id)
        return ethics_result
    except Exception as e:
        return ResponseSchema(detail=f"Error getting ethics related to paper: {str(e)}", result=None)