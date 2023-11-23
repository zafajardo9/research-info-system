from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from app.repository.auth_repo import JWTBearer, JWTRepo

from app.config import db
from app.schema import FullManuscriptCreate, FullManuscriptResponse, FullManuscriptUpdate, ResponseSchema
from app.service.manuscript_service import ManuscriptService


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
        ethics_data = await ManuscriptService.get_manuscript_by_research_paper_id(db, research_paper_id)
        if ethics_data is None:
            raise HTTPException(status_code=404, detail="No Manuscript Found")
        
        response_ethics = FullManuscriptResponse(
            id=ethics_data.id,
            created_at = ethics_data.created_at,
            research_paper_id=ethics_data.research_paper_id,
            content = ethics_data.content,
            keywords = ethics_data.keywords,
            file = ethics_data.file,
            status = ethics_data.status,
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