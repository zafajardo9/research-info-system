from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials

from app.config import db
from app.schema import FullManuscriptCreate, FullManuscriptResponse, FullManuscriptUpdate, ResponseSchema
from app.service.manuscript_service import ManuscriptService
from app.service.workflow_service import WorkflowService


router = APIRouter(
    prefix="/fullmanuscript",
    tags=['Full Manuscript'],
    dependencies=[Depends(JWTBearer())]
)


@router.post("/upload", response_model=ResponseSchema, response_model_exclude_none=True)
async def upload_ethics(
    ethics_data: FullManuscriptCreate,
):
    try:
        # Call the service method to upload ethics data
        ethics_paper = await ManuscriptService.upload_manuscript(db, ethics_data)
        
        # Return the response with the created research paper ID
        return ResponseSchema(detail=f"Manuscript data for research paper uploaded successfully", result=ethics_paper)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error uploading manuscript data: {str(e)}", result=None)


@router.get("/get_manuscript_by_research/{research_paper_id}", response_model=FullManuscriptResponse)
async def get_ethics_by_research_paper_id(research_paper_id: str):
    try:
        manuscript_data = await ManuscriptService.get_manuscript_by_research_paper_id(db, research_paper_id)
        if manuscript_data is None:
            raise HTTPException(status_code=404, detail="No Manuscript Found")
        
        response_ethics = FullManuscriptResponse(
            id=manuscript_data.id,
            modified_at=manuscript_data.modified_at,
            created_at = manuscript_data.created_at,
            research_paper_id=manuscript_data.research_paper_id,
            content = manuscript_data.content,
            keywords = manuscript_data.keywords,
            abstract = manuscript_data.abstract,
            file = manuscript_data.file,
            status = manuscript_data.status,
        )

        return response_ethics

    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)

    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error retrieving manuscript data: {str(e)}")
        return ResponseSchema(detail=f"Error retrieving manuscript data: {str(e)}", result=None)

@router.put("/update/{manuscript_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_ethics(
    manuscript_data: FullManuscriptUpdate,
    manuscript_id: str,
):
    try:
        # Call the service method to update ethics data by ethics ID
        updated_ethics = await ManuscriptService.update_manuscript(db, manuscript_data, manuscript_id)
        
        # Return the response with the updated ethics data
        return ResponseSchema(detail=f"Manuscript data for research paper {manuscript_id} updated successfully", result=updated_ethics)
    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)
    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error updating manuscript data: {str(e)}")
        return ResponseSchema(detail=f"Error updating manuscript data: {str(e)}", result=None)



@router.delete("/delete_manuscript/{manuscript_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_ethics(manuscript_id: str):
    '''
    Delete only nung manuscript
    '''
    try:
        # Call the service method to delete ethics data by research paper ID
        await ManuscriptService.delete_manuscript(db, manuscript_id)
        
        # Return the response with a success message
        return ResponseSchema(detail=f"Manuscript data for research paper {manuscript_id} deleted successfully", result=None)
    except HTTPException as e:
        return ResponseSchema(detail=f"Error deleting manuscript data: {str(e)}", result=None)
    



@router.get("/user", response_model=List[FullManuscriptResponse])
async def get_user_research_paper(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    current_user = token['user_id']

    try:
        # Call the service method to get manuscript data for the logged-in user
        manuscript_data_list = await ManuscriptService.get_manuscript_by_user(db, current_user)
        
        response_manuscript_list = []
        for manuscript_data in manuscript_data_list:
            response_manuscript = FullManuscriptResponse(
                id=manuscript_data.id,
                created_at = manuscript_data.created_at,
                modified_at=manuscript_data.modified_at,
                research_paper_id=manuscript_data.research_paper_id,
                content = manuscript_data.content,
                keywords = manuscript_data.keywords,
                abstract = manuscript_data.abstract,
                file = manuscript_data.file,
                status = manuscript_data.status,
            )
            response_manuscript_list.append(response_manuscript)

        if not response_manuscript_list:
            raise HTTPException(status_code=404, detail="No Manuscript Found for the logged-in user")

        return response_manuscript_list

    except HTTPException as e:
        return ResponseSchema(detail=f"HTTPException: {str(e)}", result=None)

    except Exception as e:
        # Print or log the full exception details for debugging
        print(f"Error getting user research papers: {str(e)}")
        return ResponseSchema(detail=f"Error getting user research papers: {str(e)}", result=None)
    
    
    


@router.get("/{workflowstep_id}/{research_id}",)
async def get_manuscript_by_workflow_step_id(workflowstep_id: str,research_id: str):
    """
    Get manuscript with workflowstep id and research that are connected
    """
    try:
        manuscript_result = await WorkflowService.get_manuscript_by_workflow_step_id(workflowstep_id,research_id)
        return manuscript_result
    except Exception as e:
        return ResponseSchema(detail=f"Error getting manuscript related to paper: {str(e)}", result=None)

