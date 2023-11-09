from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.research_paper import Author

class AuthorRepository:
    @staticmethod
    async def create(db: AsyncSession, **kwargs):
        author = Author(**kwargs)
        db.add(author)
        await db.commit()
        return author

    @staticmethod
    async def get_authors_by_research_paper(db: AsyncSession, research_paper_id: int):
        query = select(Author).where(Author.research_paper_id == research_paper_id)
        return await db.execute(query)

    @staticmethod
    async def get_by_id(db: AsyncSession, author_id: int):
        query = select(Author).where(Author.id == author_id)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, author: Author, **kwargs):
        for key, value in kwargs.items():
            setattr(author, key, value)
        await db.commit()

    @staticmethod
    async def delete(db: AsyncSession, author: Author):
        db.delete(author)
        await db.commit()