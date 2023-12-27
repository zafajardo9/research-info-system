from datetime import datetime
from itertools import groupby
from operator import attrgetter
import uuid
from sqlalchemy import delete, join, and_, update
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import select
from typing import List, Optional
import uuid
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException


from app.repository.workflow_repo import WorkflowRepository
from app.model.workflowprocess import NavigationTab, Workflow
from app.model.workflowprocess import WorkflowStep

from app.model import ResearchPaper, Ethics, FullManuscript, CopyRight
from app.schema import NavigationProcessDisplay, NavigationTabCreate, WorkflowCreate, WorkflowDetail, WorkflowGroupbyType, WorkflowStepCreate
from app.service.section_service import SectionService




class WorkflowService:

    @staticmethod
    async def create_workflow(workflow_type: str, class_id: str, user_id: str):
        workflow_id = str(uuid.uuid4())  # Generate UUID for workflow_id
        db_workflow = Workflow(id=workflow_id, type=workflow_type, class_id=class_id, user_id=user_id)
        db.add(db_workflow)
        await db.commit()
        await db.refresh(db_workflow)
        return db_workflow

    @staticmethod
    async def create_workflow_step(step_data: WorkflowStepCreate, increment: int, workflow_id: str):
        step_id = str(uuid.uuid4())  # Generate UUID for step_id
        db_workflow_step = WorkflowStep(id=step_id, **step_data.dict(), step_number= increment, workflow_id=workflow_id)
        db.add(db_workflow_step)
        await db.commit()
        await db.refresh(db_workflow_step)
        return db_workflow_step
    
    
    @staticmethod
    async def check_if_workflow_exists(type: str, class_id: str):
        workflow = await db.execute(select(Workflow).filter(Workflow.type == type, Workflow.class_id == class_id))
        return workflow.scalar() is not None
    
    @staticmethod
    async def get_workflow_by_id_with_steps(workflow_id: str):
        workflow_query = select(Workflow).where(Workflow.id == workflow_id)
        workflow = await db.execute(workflow_query)
        workflow = workflow.scalar()

        if not workflow:
            return None  # Return None when the workflow is not found

        steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
        steps = await db.execute(steps_query)
        steps = steps.scalars().all()

        workflow_detail = WorkflowDetail(
            id=workflow.id,
            course=workflow.course,
            year=workflow.year,
            type=workflow.type,
            user_id=workflow.user_id,
            steps=steps
        )

        return workflow_detail
# ================================================ FOR NAVIGATIONS
    # @staticmethod
    # async def create_process_role(navigation_tab: NavigationTabCreate):
    #     process_id = str(uuid.uuid4())
    #     db_process = NavigationTab(id=process_id, **navigation_tab.dict())
    #     db.add(db_process)
    #     await db.commit()
    #     await db.refresh(db_process)
    #     return db_process
    
    
    @staticmethod
    async def create_process_role(navigation_tab: NavigationTabCreate):
        created_processes = []
        for class_id in navigation_tab.class_id:
            process_id = str(uuid.uuid4())
            # Create a process for each class_id
            db_process = NavigationTab(id=process_id, role=navigation_tab.role, type=navigation_tab.type, class_id=class_id,
                                    has_submitted_proposal=navigation_tab.has_submitted_proposal,
                                    has_pre_oral_defense_date=navigation_tab.has_pre_oral_defense_date,
                                    has_submitted_ethics_protocol=navigation_tab.has_submitted_ethics_protocol,
                                    has_submitted_full_manuscript=navigation_tab.has_submitted_full_manuscript,
                                    has_set_final_defense_date=navigation_tab.has_set_final_defense_date,
                                    has_submitted_copyright=navigation_tab.has_submitted_copyright)
            db.add(db_process)
            await db.commit()
            await db.refresh(db_process)
            created_processes.append(db_process)
        return created_processes
    
    
    
    @staticmethod
    async def update_process_role(id: str, navigation_tab: NavigationTabCreate):
        result = await db.execute(select(NavigationTab).where(NavigationTab.id == id))
        update_process = result.scalar_one_or_none()

        if update_process:
            # Update the fields with new values
            for key, value in navigation_tab.dict().items():
                setattr(update_process, key, value)

            await db.commit()
            await db.refresh(update_process)
            return update_process
        else:
            raise HTTPException(status_code=404, detail="Process set not found")
        
    @staticmethod
    async def delete_process_by_id(id: str):
            # Delete workflow steps
        await db.execute(delete(NavigationTab).where(NavigationTab.id == id))

        return True
        
    @staticmethod
    async def display_process():
        result = await db.execute(select(NavigationTab))
        update_process = result.scalars().all()
        
        
            # Convert SQLAlchemy models to Pydantic models
        display_processes = [NavigationProcessDisplay(
            role=process.role,
            type=process.type,
            class_id=process.class_id,
            has_submitted_proposal=process.has_submitted_proposal,
            has_pre_oral_defense_date=process.has_pre_oral_defense_date,
            has_submitted_ethics_protocol=process.has_submitted_ethics_protocol,
            has_submitted_full_manuscript=process.has_submitted_full_manuscript,
            has_set_final_defense_date=process.has_set_final_defense_date,
            has_submitted_copyright=process.has_submitted_copyright,
        ) for process in update_process]


        return display_processes
    
    @staticmethod
    async def display_process_by_type():
        # Default ordering by id, you can change it to any column you want
        result = await db.execute(select(NavigationTab))
        processes = result.scalars().all()

        # Group processes by type
        grouped_processes = {key: list(group) for key, group in groupby(processes, key=attrgetter('type'))}

        # Convert SQLAlchemy models to Pydantic models for each type
        display_processes_by_type = {
            type_: [NavigationProcessDisplay(
                role=process.role,
                type=process.type,
                class_id=process.class_id,
                has_submitted_proposal=process.has_submitted_proposal,
                has_pre_oral_defense_date=process.has_pre_oral_defense_date,
                has_submitted_ethics_protocol=process.has_submitted_ethics_protocol,
                has_submitted_full_manuscript=process.has_submitted_full_manuscript,
                has_set_final_defense_date=process.has_set_final_defense_date,
                has_submitted_copyright=process.has_submitted_copyright,
            ) for process in processes] for type_, processes in grouped_processes.items()
        }

        return display_processes_by_type

# =================================================
    @staticmethod
    async def get_workflow_with_steps(user_id: str):
        workflows_query = select(Workflow).where(Workflow.user_id == user_id)
        workflows = await db.execute(workflows_query)
        workflows = workflows.scalars().all()

        if not workflows:
            return []  # Return an empty list when no workflows are found

        workflows_with_steps = []
        for workflow in workflows:
            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps = await db.execute(steps_query)
            steps = steps.scalars().all()

            workflow_detail = WorkflowDetail(id=workflow.id, course=workflow.course, year=workflow.year, type=workflow.type, user_id=workflow.user_id, steps=steps)
            workflows_with_steps.append(workflow_detail)

        return workflows_with_steps
    
    
    #Ginamit lang para sa update para mas makuha ang mga data
    @staticmethod
    async def get_workflow_by_id_with_steps(workflow_id: str):
        workflow_query = select(Workflow).where(Workflow.id == workflow_id)
        workflow = await db.execute(workflow_query)
        workflow = workflow.scalars().first()

        if not workflow:
            return None

        steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
        steps = await db.execute(steps_query)
        steps = steps.scalars().all()
        
        class_data = await SectionService.what_section_course(workflow.class_id)

        workflow_detail = WorkflowDetail(
                id=workflow.id, 
                type=workflow.type, 
                class_id= workflow.class_id,
                course=class_data.course, 
                section=class_data.section,
                user_id=workflow.user_id, 
                steps=steps)
        
        return workflow_detail
    

    @staticmethod
    async def get_workflow_all():
        workflows_query = select(Workflow)
        workflows = await db.execute(workflows_query)
        workflows = workflows.scalars().all()

        if not workflows:
            return []  # Return an empty list when no workflows are found

        workflows_with_steps = []
        for workflow in workflows:
            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps = await db.execute(steps_query)
            steps = steps.scalars().all()
            class_data = await SectionService.what_section_course(workflow.class_id)
            
            
            workflow_detail = WorkflowDetail(
                    id=workflow.id, 
                    class_id=workflow.class_id, 
                    section=class_data.section, 
                    course=class_data.course, 
                    type=workflow.type, 
                    user_id=workflow.user_id, 
                    steps=steps)
            workflows_with_steps.append(workflow_detail)

        return workflows_with_steps
    
    
    @staticmethod
    async def get_workflow_all_by_type(type: str):
        workflows_query = select(Workflow).where(Workflow.type == type)
        workflows = await db.execute(workflows_query)
        workflows = workflows.scalars().all()

        if not workflows:
            return []  # Return an empty list when no workflows are found

        workflows_with_steps = []
        for workflow in workflows:
            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps = await db.execute(steps_query)
            steps = steps.scalars().all()
            
            class_data = await SectionService.what_section_course(workflow.class_id)

            workflow_detail = WorkflowDetail(
                        id=workflow.id, 
                        type=workflow.type, 
                        class_id=workflow.class_id,
                        course=class_data.course,
                        section=class_data.section,
                        user_id=workflow.user_id, 
                        steps=steps)
            workflows_with_steps.append(workflow_detail)

        return workflows_with_steps
    
    # @staticmethod
    # async def get_workflow_all_by_type(type: str):
    #     workflows_query = select(Workflow)
    #     workflows = await db.execute(workflows_query)
    #     workflows = workflows.scalars().all()

    #     if not workflows:
    #         return [] # Return an empty list when no workflows are found

    #     # Sort workflows by type
    #     workflows.sort(key=attrgetter('type'))

    #     # Group workflows by type
    #     workflow_groups = []
    #     for key, group in groupby(workflows, key=attrgetter('type')):
    #         for workflow in group:
    #             steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
    #             steps = await db.execute(steps_query)
    #             steps = steps.scalars().all()

    #             workflow_detail = WorkflowDetail(id=workflow.id, course=workflow.course, year=workflow.year, type=workflow.type, user_id=workflow.user_id, steps=steps)
    #             workflow_group = WorkflowGroupbyType(type=key, workflows=[workflow_detail])
    #             workflow_groups.append(workflow_group)

    #     return workflow_groups


    #CHECK 
    # todo FIX THE IDEA LUMA TO
    @staticmethod
    async def get_my_workflow(user_course: str, user_section: str):

        query = (
            select(Workflow, WorkflowStep)
            .join(WorkflowStep, Workflow.id == WorkflowStep.workflow_id)
            .where(and_(Workflow.course == user_course, Workflow.year == user_section))
            .distinct(Workflow.id, Workflow.course, Workflow.year, Workflow.type, Workflow.user_id)
        )

        workflows = await db.execute(query)
        workflows = workflows.scalars().all()

        if not workflows:
            return []  # Return an empty list when no workflows are found

        workflows_with_steps = []
        for workflow in workflows:
            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps = await db.execute(steps_query)
            steps = steps.scalars().all()

            workflow_detail = WorkflowDetail(id=workflow.id, course=workflow.course, year=workflow.year, type=workflow.type, user_id=workflow.user_id, steps=steps)
            workflows_with_steps.append(workflow_detail)

        return workflows_with_steps    
    
    
    
        
    #BREAKDOWN BETWEEN THE WORKFLOW DATA AND THE STEPS
    @staticmethod
    async def get_workflow_id(workflow_id: str):
        workflow_query = select(Workflow).where(Workflow.id == workflow_id)
        workflow = await db.execute(workflow_query)
        workflow = workflow.scalars().first()

        if not workflow:
            return None

        return workflow
    
    @staticmethod
    async def get_workflow_steps_id(workflow_id: str):


        steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id)
        steps = await db.execute(steps_query)
        steps = steps.scalars().all()

        return steps

    
    @staticmethod
    async def update_workflow_with_steps(workflow_id: str, workflow_data: WorkflowCreate, steps_data: List[WorkflowStepCreate]):
        workflow = await WorkflowService.get_workflow_id(workflow_id)
        if workflow:
            for key, value in dict(workflow_data).items():
                setattr(workflow, key, value)

            # Delete all existing steps
            await db.execute(delete(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id))

            # Insert new steps
            for step_data in steps_data:
                await WorkflowService.create_workflow_step(step_data, workflow.id)

            await db.commit()
            await db.refresh(workflow)
            return workflow
        return None
#==============deleting


    @staticmethod
    async def delete_workflow_by_id(workflow_id: str):
        workflow = await WorkflowService.get_workflow_by_id_with_steps(workflow_id)

        if not workflow:
            return False  # Return False when the workflow is not found


            # Delete workflow steps
        await db.execute(delete(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id))

            # Delete the workflow itself
        await db.execute(delete(Workflow).where(Workflow.id == workflow.id))

        return True
    
    @staticmethod
    async def delete_workflowstep_by_id(workflow_step_id: str):
            # Delete workflow steps
        await db.execute(delete(WorkflowStep).where(WorkflowStep.id == workflow_step_id))
        return True

# 28914385-40fd-43f2-ad5c-898b9263f08f


    @staticmethod
    async def get_research_paper_by_workflow_step_id(workflow_step_id: str):
        research_paper_result = await db.execute(
            select(ResearchPaper).filter(ResearchPaper.workflow_step_id == workflow_step_id)
        )
        research_paper = research_paper_result.scalars().first()
        if research_paper:
            return {
                "id": research_paper.id,
                "title": research_paper.title,
                "research_type": research_paper.research_type,
                "submitted_date": research_paper.submitted_date,
                "status": research_paper.status,
                "file_path": research_paper.file_path,
                "research_adviser": research_paper.research_adviser,
            }
        else:
            return None
        
    @staticmethod
    async def get_research_paper_by_step_and_id(workflow_step_id: str, research_paper_id: str):
        research_paper_result = await db.execute(
            select(ResearchPaper)
            .filter(ResearchPaper.workflow_step_id == workflow_step_id)
            .filter(ResearchPaper.id == research_paper_id)
        )
        research_paper = research_paper_result.scalars().first()
        if research_paper:
            return {
                "id": research_paper.id,
                "title": research_paper.title,
                "research_type": research_paper.research_type,
                "submitted_date": research_paper.submitted_date,
                "status": research_paper.status,
                "file_path": research_paper.file_path,
                "research_adviser": research_paper.research_adviser,
            }
        else:
            return None
        
    
    @staticmethod
    async def get_ethics_by_workflow_step_id(workflow_step_id: str, research_paper_id: str):
        ethics_result = await db.execute(
            select(Ethics)
            .filter(Ethics.workflow_step_id == workflow_step_id)
            .filter(Ethics.research_paper_id == research_paper_id)
        )
        ethics = ethics_result.scalars().first() # Extract the Ethics object from the ChunkedIteratorResult object
        if ethics:
            return {
                "id": ethics.id,
                "letter_of_intent": ethics.letter_of_intent,
                "urec_9": ethics.urec_9,
                "urec_10": ethics.urec_10,
                "urec_11": ethics.urec_11,
                "urec_12": ethics.urec_12,
                "certificate_of_validation": ethics.certificate_of_validation,
                "co_authorship": ethics.co_authorship,
                "status": ethics.status
            }
        else:
            return None
        
        
    @staticmethod
    async def get_copyright_by_workflow_step_id(workflow_step_id: str, research_paper_id: str):
        copyright_result = await db.execute(
            select(CopyRight)
            .filter(CopyRight.workflow_step_id == workflow_step_id)
            .filter(CopyRight.research_paper_id == research_paper_id)
        )
        copyright = copyright_result.scalars().first()
        if copyright:
            return {
                "id": copyright.id,
                "letter_of_intent": copyright.letter_of_intent,
                "urec_9": copyright.urec_9,
                "urec_10": copyright.urec_10,
                "urec_11": copyright.urec_11,
                "urec_12": copyright.urec_12,
                "certificate_of_validation": copyright.certificate_of_validation,
                "co_authorship": copyright.co_authorship,
                "status": copyright.status
            }
            
        else:
            return None
        
    @staticmethod
    async def get_manuscript_by_workflow_step_id(workflow_step_id: str, research_paper_id: str):
        manuscript_result = await db.execute(
            select(FullManuscript)
            .filter(FullManuscript.workflow_step_id == workflow_step_id)
            .filter(FullManuscript.research_paper_id == research_paper_id)
        )
        manuscript = manuscript_result.scalars().first()
        if manuscript:
            return {
                "id": manuscript.id,
                "content": manuscript.content,
                "keywords": manuscript.keywords,
                "file": manuscript.file,
                "abstract": manuscript.abstract,
                "status": manuscript.status,
            }
            
        else:
            return None
    

    @staticmethod
    async def get_my_workflow_by_id(workflow_id: str):
        query = (
            select(Workflow)
            .where(Workflow.id == workflow_id)
        )

        workflows = await db.execute(query)
        workflows = workflows.scalars().first()

        if not workflows:
            raise HTTPException(status_code=404, detail="Workflow not found")

        steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id)
        steps = await db.execute(steps_query)
        steps = steps.scalars().all()

        workflow_with_steps = {
            'id': workflows.id,
            'course': workflows.course,
            'year': workflows.year,
            'type': workflows.type,
            'user_id': workflows.user_id,
            'steps': []
        }

        for step in steps:
            research_paper_detail = await WorkflowService.get_research_paper_by_workflow_step_id(step.id)
            if research_paper_detail is not None and research_paper_detail["id"] is not None:
                ethics_detail = await WorkflowService.get_ethics_by_workflow_step_id(step.id, research_paper_detail["id"])
                copyright_detail = await WorkflowService.get_copyright_by_workflow_step_id(step.id, research_paper_detail["id"])
                manuscript_detail = await WorkflowService.get_manuscript_by_workflow_step_id(step.id, research_paper_detail["id"])
            else:
                ethics_detail = copyright_detail = manuscript_detail = {"id": None}

            step_detail = {
                'step_number': step.step_number,
                'id': step.id,
                'name': step.name,
                'description': step.description,
                'workflow_id': step.workflow_id,
                'research_paper': research_paper_detail,
                'ethics': ethics_detail,
                'copyright': copyright_detail,
                'manuscript': manuscript_detail
            }

            workflow_with_steps['steps'].append(step_detail)

        return workflow_with_steps