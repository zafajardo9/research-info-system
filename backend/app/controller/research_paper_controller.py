

from typing import List
from app.repository.research_paper_repo import ResearchPaperRepository
from fastapi import APIRouter, Depends, Security, HTTPException
from app.schema import ResponseSchema, ResearchPaperSchema
from app.repository.auth_repo import JWTBearer

router = APIRouter(
    prefix="/research-papers",
    tags=["Research Papers"],
    dependencies=[Depends(JWTBearer())]
)


# CREATE
@router.post("", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_research_paper(
    create_form: ResearchPaperSchema
):
    research_paper_id = await ResearchPaperRepository.create_research_paper(create_form)
    return ResponseSchema(detail="Successfully created data with ID: " + str(research_paper_id))

# READ
@router.get("/{research_paper_id}", response_model=ResearchPaperSchema)
async def get_research_paper(research_paper_id: int):
    research_paper = await ResearchPaperRepository.get_by_id(research_paper_id)
    if research_paper:
        return research_paper
    raise HTTPException(status_code=404, detail="Research paper not found")

# UPDATE
@router.put("/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_research_paper(research_paper_id: int, update_form: ResearchPaperSchema):
    await ResearchPaperRepository.update(research_paper_id, update_form)
    return ResponseSchema(detail="Successfully updated research paper with ID: " + str(research_paper_id))

# DELETE
@router.delete("/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_research_paper(research_paper_id: int):
    await ResearchPaperRepository.delete(research_paper_id)
    return ResponseSchema(detail="Successfully deleted research paper with ID: " + str(research_paper_id))




# =====================================================



# @router.get("/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
# async def get_research_paper_by_id(research_paper_id: int):
#     research_paper = await ResearchPaperService.get_research_paper_by_id(research_paper_id)
#     if research_paper:
#         return ResponseSchema(detail="Fetched research paper by ID", result=research_paper)
#     else:
#         raise HTTPException(status_code=404, detail="Research paper not found")

# @router.put("/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
# async def update_research_paper(
#     research_paper_id: int,
#     research_paper_data: ResearchPaperSchema,
#     credentials=Depends(JWTBearer())
# ):
#     try:
#         research_paper = await ResearchPaperService.update_research_paper(
#             research_paper_id,
#             research_paper_data.title,
#             research_paper_data.content,
#             research_paper_data.adviser_id,
#             research_paper_data.author_ids
#         )
#         return ResponseSchema(detail="Research paper updated successfully!", result=research_paper)
#     except HTTPException as e:
#         return ResponseSchema(detail=e.detail, result=None), e.status_code

# @router.delete("/{research_paper_id}", response_model=ResponseSchema, response_model_exclude_none=True)
# async def delete_research_paper(research_paper_id: int, credentials=Depends(JWTBearer())):
#     try:
#         await ResearchPaperService.delete_research_paper(research_paper_id)
#         return ResponseSchema(detail="Research paper deleted successfully!")
#     except HTTPException as e:
#         return ResponseSchema(detail=e.detail, result=None), e.status_code
