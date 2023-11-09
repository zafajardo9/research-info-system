
from typing import List
from app.schema import AuthorSchema, ResearchPaperSchema

from sqlalchemy import insert, update, delete, or_, text, func, column
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.research_paper import ResearchPaper, Author

from app.config import db, commit_rollback




class ResearchPaperRepository:
    
    @staticmethod
    async def create_research_paper(create_form: ResearchPaperSchema):
        """Create a research paper without authors and return its ID."""
        research_paper = ResearchPaper(
            title=create_form.title,
            content=create_form.content,
            research_adviser=create_form.research_adviser
        )
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InphZmFqYXJkbyIsImV4cCI6MTY5OTE5MjAwN30.SYtFO7IXhJiLiEDU9Lj60_PysQhUfuS9F3_dWkZt-u8
        db.add(research_paper)
        await commit_rollback()

        return research_paper.id

    @staticmethod
    async def add_authors_to_research_paper(research_paper_id: int, author_data: List[AuthorSchema]):
        """Add authors to an existing research paper by its ID."""
        # Retrieve the existing research paper by ID
        research_paper = db.get(ResearchPaper, research_paper_id)

        if research_paper is None:
            # Handle the case where the research paper doesn't exist
            raise ValueError("Research paper with the provided ID does not exist")

        # Create a list to hold the author instances
        author_instances = []

        # Loop through author data and create Author instances
        for author_data in author_data:
            author = Author(
                user_id=author_data.user_id,
                name=author_data.name,
                research_paper_id=research_paper.id  # Set the research paper ID
            )
            author_instances.append(author)

        # Add authors to the research paper
        research_paper.authors.extend(author_instances)

        # Commit the changes to add authors to the research paper
        await db.commit()

    @staticmethod
    async def get_by_id(research_paper_id: int):
        """Retrieve a research paper by ID."""
        query = select(ResearchPaper).where(ResearchPaper.id == research_paper_id)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update(research_paper_id: int, update_form: ResearchPaperSchema):
        """Update a research paper."""
        query = select(ResearchPaper).where(ResearchPaper.id == research_paper_id)
        existing_research_paper = (await db.execute(query)).scalar_one_or_none()

        if existing_research_paper:
            for field, value in update_form.dict().items():
                setattr(existing_research_paper, field, value)
            await commit_rollback()



#================ DELETE ===================
    @staticmethod
    async def delete(research_id: int):
        """ delete research data by id """

        query = delete(ResearchPaper).where(ResearchPaper.id == research_id)
        await db.execute(query)
        await commit_rollback()
        
        
        #================= WILL BE PUTTING A MORE GOOD WAY TO SORT DATA ====================

    # @staticmethod
    # async def delete(research_id: int):
    #     """Delete research data by ID."""
    #     query = select(ResearchPaper).where(ResearchPaper.id == research_id)
    #     research_paper = (await db.execute(query)).scalar_one_or_none()

    #     if research_paper:
    #         db.delete(research_paper)
    #         await commit_rollback()
