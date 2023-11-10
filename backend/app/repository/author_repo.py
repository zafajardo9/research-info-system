from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.research_paper import Author
from app.config import db
from app.schema import AuthorSchema

class AuthorRepository:
    @staticmethod
    async def create(author: AuthorSchema):
        author = Author(**author.dict())
        db.add(author)
        await db.commit()
        await db.refresh(author)
        return author

    @staticmethod
    async def get_by_id(id: int):
        query = select(Author).where(Author.id == id)
        result = await db.execute(query)
        author = result.scalar_one_or_none()
        return author

    @staticmethod
    async def get_all():
        query = select(Author)
        result = await db.execute(query)
        authors = result.scalars().all()
        return authors

    @staticmethod
    async def update(id: int, updated_author: Author):
        db.update(Author).where(Author.id == id).values(name=updated_author.name)
        await db.commit()

    @staticmethod
    async def delete(id: int):
        db.delete(Author).where(Author.id == id)
        await db.commit()