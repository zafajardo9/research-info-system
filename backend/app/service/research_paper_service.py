from app.repository.research_paper_repo import ResearchPaperRepository
from app.model.research_paper import ResearchPaper
from app.schema import ResearchPaperSchema

class ResearchPaperService:
    @staticmethod
    async def create_research_paper(research_paper: ResearchPaperSchema):
        return await ResearchPaperRepository.create(research_paper)

    @staticmethod
    async def get_research_paper_by_id(id: int):
        return await ResearchPaperRepository.get_by_id(id)

    @staticmethod
    async def get_all_research_papers():
        return await ResearchPaperRepository.get_all()

    @staticmethod
    async def update_research_paper(id: int, updated_paper: ResearchPaper):
        return await ResearchPaperRepository.update(id, updated_paper)

    @staticmethod
    async def delete_research_paper(id: int):
        return await ResearchPaperRepository.delete(id)
