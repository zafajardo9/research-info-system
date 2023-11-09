# from typing import List
# from app.model.research_paper import ResearchPaper
# from app.model.users import Users
# from app.repository.research_paper_repo import ResearchPaperRepository
# from app.repository.users import UsersRepository
# from app.schema import ResearchPaperSchema
# from fastapi import HTTPException

# class ResearchPaperService:
#     @staticmethod
#     async def create_research_paper(research_paper_data: ResearchPaperSchema, adviser_id: int, author_ids: List[int]):
#         # Check if the adviser exists
#         adviser = await UsersRepository.get_by_id(adviser_id)
#         if not adviser or adviser.roles != "faculty":
#             raise HTTPException(status_code=404, detail="Adviser not found or invalid role!")

#         # Check if the authors exist
#         authors = await UsersRepository.get_by_ids(author_ids)
#         for author in authors:
#             if author.roles != "student":
#                 raise HTTPException(status_code=404, detail="Invalid author role!")

#         # Create the research paper
#         research_paper = await ResearchPaperRepository.create(
#             title=research_paper_data.title, 
#             content=research_paper_data.content, 
#             adviser_id=adviser_id
#         )

#         # Add authors to the research paper
#         for author in authors:
#             await research_paper.add_author(author)

#         return research_paper

#     # ===========FOR READING THE TABLE==============
#     @staticmethod
#     async def get_all_research_papers():
#         return await ResearchPaperRepository.get_all()

#     @staticmethod
#     async def get_research_paper_by_id(research_paper_id: int):
#         return await ResearchPaperRepository.get_by_id(research_paper_id)

#     #========EDITING OR UPDATE=================
#     @staticmethod
#     async def update_research_paper(research_paper_id: int, research_paper_data: ResearchPaperSchema, adviser_id: int, author_ids: List[int]):
#         # Check if the adviser exists
#         adviser = await UsersRepository.get_by_id(adviser_id)
#         if not adviser or adviser.roles != "faculty":
#             raise HTTPException(status_code=404, detail="Adviser not found or invalid role!")

#         # Check if the authors exist
#         authors = await UsersRepository.get_by_ids(author_ids)
#         for author in authors:
#             if author.roles != "student":
#                 raise HTTPException(status_code=404, detail="Invalid author role!")

#         # Retrieve the research paper
#         research_paper = await ResearchPaperRepository.get_by_id(research_paper_id)
#         if not research_paper:
#             raise HTTPException(status_code=404, detail="Research paper not found!")

#         # Update the research paper
#         await ResearchPaperRepository.update(
#             research_paper, 
#             title=research_paper_data.title, 
#             content=research_paper_data.content, 
#             adviser_id=adviser_id
#         )

#         # Update the authors
#         await research_paper.update_authors(authors)

#         return research_paper

#     #============== DELETE =========
#     @staticmethod
#     async def delete_research_paper(research_paper_id: int):
#         # Retrieve the research paper
#         research_paper = await ResearchPaperRepository.get_by_id(research_paper_id)
#         if not research_paper:
#             raise HTTPException(status_code=404, detail="Research paper not found!")

#         # Delete the research paper
#         await ResearchPaperRepository.delete(research_paper)
