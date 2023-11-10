from app.repository.author_repo import AuthorRepository
from app.model.research_paper import Author
from app.schema import AuthorSchema

class AuthorService:
    @staticmethod
    async def create_author(author: AuthorSchema):
        return await AuthorRepository.create(author)

    @staticmethod
    async def get_author_by_id(id: int):
        return await AuthorRepository.get_by_id(id)

    @staticmethod
    async def get_all_authors():
        return await AuthorRepository.get_all()

    @staticmethod
    async def update_author(id: int, updated_author: Author):
        return await AuthorRepository.update(id, updated_author)

    @staticmethod
    async def delete_author(id: int):
        return await AuthorRepository.delete(id)
