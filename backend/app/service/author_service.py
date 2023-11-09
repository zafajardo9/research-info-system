from app.model.research_paper import Author
from app.repository.author_repo import AuthorRepository
from app.schema import AuthorSchema
from fastapi import HTTPException

class AuthorService:
    
    # ========= CREATE ===========
    @staticmethod
    async def create_author(author_data: AuthorSchema):
        # Create a new author
        author = await AuthorRepository.create(**author_data.dict())
        return author
    
    # ======= READ ==========
    @staticmethod
    async def get_authors_by_research_paper(research_paper_id: int):
        return await AuthorRepository.get_authors_by_research_paper(research_paper_id)
    
    #====== UPDATE ========
    @staticmethod
    async def update_author(author_id: int, user_id: int, research_paper_id: int):
        # Retrieve the author
        author = await AuthorRepository.get_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found!")

        # Update the author
        await AuthorRepository.update(author, user_id=user_id, research_paper_id=research_paper_id)

        return author
    
    #======= DELETE ============
    @staticmethod
    async def delete_author(author_id: int):
        # Retrieve the author
        author = await AuthorRepository.get_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found!")

        # Delete the author
        await AuthorRepository.delete(author)
