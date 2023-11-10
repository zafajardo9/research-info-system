from fastapi import APIRouter, Depends, HTTPException
from app.schema import AuthorSchema, ResponseSchema
from app.service.author_service import AuthorService

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)

@router.post("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_author(author: AuthorSchema):
    created_author = await AuthorService.create_author(author)
    return ResponseSchema(detail="Author created successfully!", result=created_author)

@router.get("/{author_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_author_by_id(author_id: int):
    author = await AuthorService.get_author_by_id(author_id)
    if author:
        return ResponseSchema(detail="Fetched author by ID", result=author)
    else:
        raise HTTPException(status_code=404, detail="Author not found")

@router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_authors():
    authors = await AuthorService.get_all_authors()
    return ResponseSchema(detail="Fetched all authors", result=authors)

@router.put("/{author_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_author(author_id: int, updated_author: AuthorSchema):
    await AuthorService.update_author(author_id, updated_author)
    return ResponseSchema(detail="Author updated successfully!")

@router.delete("/{author_id}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_author(author_id: int):
    await AuthorService.delete_author(author_id)
    return ResponseSchema(detail="Author deleted successfully!")
