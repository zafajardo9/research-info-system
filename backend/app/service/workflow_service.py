from collections import defaultdict
from datetime import datetime
from itertools import groupby
import logging
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
from sqlalchemy.exc import IntegrityError


from app.repository.workflow_repo import WorkflowRepository
from app.model.workflowprocess import NavigationClass, NavigationTab, Workflow, WorkflowClass
from app.model.workflowprocess import WorkflowStep

from app.model import ResearchPaper, Ethics, FullManuscript, CopyRight
from app.schema import FLOW2, NavigationProcessDisplay, NavigationTabCreate, NavigationTabUpdate, WorkflowCreate, WorkflowDetail, WorkflowDetailSpecific, WorkflowDetailWithStatus, WorkflowGroupbyType, WorkflowResearchInfo, WorkflowResearchInfoStep, WorkflowResponse, WorkflowStepCreate, WorkflowStepDetailWithStatus, WorkflowUpdate
from app.service.section_service import SectionService
from app.model.student import Class, Student
from app.model.researchdef import ResearchDefense
from app.model.faculty import Faculty
from app.model.research_paper import Author
from app.model.users import Users
from app.model import SetDefense, SetDefenseClass




class WorkflowService:

    @staticmethod
    async def create_workflow(workflow_type: str, user_id: str):
        workflow_id = str(uuid.uuid4())  # Generate UUID for workflow_id
        db_workflow = Workflow(id=workflow_id, type=workflow_type, user_id=user_id)
        db.add(db_workflow)
        await db.commit()
        await db.refresh(db_workflow)
        return db_workflow

    @staticmethod
    async def create_workflow_step(step_data: WorkflowStepCreate, workflow_id: str):
        step_id = str(uuid.uuid4())  # Generate UUID for step_id
        db_workflow_step = WorkflowStep(id=step_id, **step_data.dict(), workflow_id=workflow_id)
        db.add(db_workflow_step)
        await db.commit()
        await db.refresh(db_workflow_step)
        return db_workflow_step
    
    
    @staticmethod
    async def create_workflow_class_association(workflow_id: str, class_id: str):
        existing_association = await db.execute(
            select(WorkflowClass).filter_by(workflow_id=workflow_id, class_id=class_id)
        )

        asoc = existing_association.scalar()

        if asoc:
            logging.warning(f"Association already exists for workflow {workflow_id} and class {class_id}")
            return asoc  # Return the existing association instead of creating a new one

        # Create a new association if it doesn't exist
        id_class = str(uuid.uuid4())
        workflow_class = WorkflowClass(id=id_class, workflow_id=workflow_id, class_id=class_id)
        db.add(workflow_class)
        await db.commit()
        await db.refresh(workflow_class)
        return workflow_class
    

    # @staticmethod
    # async def check_if_workflow_exists(type: str, class_id: str):
    #     workflow = await db.execute(select(Workflow).filter(Workflow.type == type, Workflow.class_id == class_id))
    #     return workflow.scalar() is not None
    
    @staticmethod
    async def check_if_workflow_type_exist(type: str):
        workflow = await db.execute(select(Workflow).filter(Workflow.type == type))
        return workflow.scalar() is not None
    

    
    
    @staticmethod
    async def update_workflow(workflow_id: str, update_data: WorkflowUpdate):
        db_workflow = await Workflow.get(workflow_id)
        if not db_workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_workflow, key, value)

        db.add(db_workflow)
        await db.commit()
        await db.refresh(db_workflow)
        return db_workflow
    
    
    @staticmethod
    async def get_workflow_all():
        workflows_query = select(Workflow)
        workflows = await db.execute(workflows_query)
        workflows = workflows.scalars().all()

        if not workflows:
            return [] # Return an empty list when no workflows are found

        workflows_with_details = []
        for workflow in workflows:
            # Get class data
            class_query = (select(WorkflowClass.id, WorkflowClass.class_id, Class.section, Class.course)
                        .join(Class, WorkflowClass.class_id == Class.id)
                        .where(WorkflowClass.workflow_id == workflow.id))
            class_data = await db.execute(class_query)
            class_data = class_data.fetchall()
            

            # Get steps data
            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps_data = await db.execute(steps_query)
            steps_data = steps_data.scalars().all()
            
            print(steps_data)
            steps_data = [{
                "id": row.id,
                "name": row.name,
                "description": row.description
            } for row in steps_data]

            workflow_detail = {
                "id": workflow.id,
                "type": workflow.type,
                "user_id": workflow.user_id,
                "class_": class_data,
                "steps": steps_data
                
            }
            workflows_with_details.append(workflow_detail)

        return workflows_with_details
    
    
    @staticmethod
    async def get_workflow_all_by_type(type: str):
        workflows_query = select(Workflow).where(Workflow.type == type)
        workflows = await db.execute(workflows_query)
        workflows = workflows.scalars().all()

        if not workflows:
            return [] # Return an empty list when no workflows are found

        workflows_with_details = []
        for workflow in workflows:
            # Get class data
            class_query = (select(WorkflowClass.id, WorkflowClass.class_id, Class.section, Class.course)
                        .join(Class, WorkflowClass.class_id == Class.id)
                        .where(WorkflowClass.workflow_id == workflow.id))
            class_data = await db.execute(class_query)
            class_data = class_data.fetchall()
            

            # Get steps data
            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps_data = await db.execute(steps_query)
            steps_data = steps_data.scalars().all()
            
            print(steps_data)
            steps_data = [{
                "id": row.id,
                "name": row.name,
                "description": row.description
            } for row in steps_data]

            workflow_detail = {
                "id": workflow.id,
                "type": workflow.type,
                "user_id": workflow.user_id,
                "class_": class_data,
                "steps": steps_data
                
            }
            workflows_with_details.append(workflow_detail)

        return workflows_with_details
    
    @staticmethod
    async def get_workflow_all_by_id(id: str):
        workflows_query = select(Workflow).where(Workflow.id == id)
        workflows = await db.execute(workflows_query)
        workflows = workflows.scalars().all()

        if not workflows:
            return [] # Return an empty list when no workflows are found

        workflows_with_details = []
        for workflow in workflows:
            # Get class data
            class_query = (select(WorkflowClass.id, WorkflowClass.class_id, Class.section, Class.course)
                        .join(Class, WorkflowClass.class_id == Class.id)
                        .where(WorkflowClass.workflow_id == workflow.id))
            class_data = await db.execute(class_query)
            class_data = class_data.fetchall()

            # Get steps data
            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps_data = await db.execute(steps_query)
            steps_data = steps_data.scalars().all()
            
            print(steps_data)
            steps_data = [{
                "id": row.id,
                "name": row.name,
                "description": row.description
            } for row in steps_data]

            workflow_detail = {
                "id": workflow.id,
                "type": workflow.type,
                "user_id": workflow.user_id,
                "class_": class_data,
                "steps": steps_data
                
            }
            workflows_with_details.append(workflow_detail)

        return workflows_with_details
    
    
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
        process_id = str(uuid.uuid4())
        db_process = NavigationTab(
            id=process_id,
            role=navigation_tab.role,
            type=navigation_tab.type,
            has_submitted_proposal=navigation_tab.has_submitted_proposal,
            has_pre_oral_defense_date=navigation_tab.has_pre_oral_defense_date,
            has_submitted_ethics_protocol=navigation_tab.has_submitted_ethics_protocol,
            has_submitted_full_manuscript=navigation_tab.has_submitted_full_manuscript,
            has_set_final_defense_date=navigation_tab.has_set_final_defense_date,
            has_submitted_copyright=navigation_tab.has_submitted_copyright,
        )
        db.add(db_process)
        await db.commit()
        await db.refresh(db_process)

        # Create NavigationClass entries for each class_id
        created_processes = []
        for class_id in navigation_tab.class_id:
            navigation_class_entry = await WorkflowService.create_process_role_class_assoc(process_id, class_id)
            created_processes.append(navigation_class_entry)

        return created_processes
    
    @staticmethod
    async def create_process_role_class_assoc(process_id: str, class_id: str):
        try:
            # Retrieve the navigation record
            navigation_record = await db.execute(select(NavigationTab).where(NavigationTab.id == process_id))
            navigation_record = navigation_record.scalar()

            if not navigation_record:
                raise HTTPException(status_code=404, detail=f"Navigation with id {process_id} not found.")


            navigation_class_entry = NavigationClass(id=str(uuid.uuid4()), navigation_id=process_id, class_id=class_id)
            db.add(navigation_class_entry)
            await db.commit()
            return navigation_class_entry
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    @staticmethod
    async def update_process_role(id: str, navigation_tab_update: NavigationTabUpdate):
        # Get the NavigationTab entry
        navigation_tab = await db.get(NavigationTab, id)
        
        if not navigation_tab:
            raise HTTPException(status_code=404, detail=f"Navigation with id {id} not found.")

        # Update the fields based on the received data
        for field, value in navigation_tab_update.dict(exclude_unset=True).items():
            setattr(navigation_tab, field, value)

        await db.commit()
        await db.refresh(navigation_tab)

        return navigation_tab

    @staticmethod
    async def get_workflows_by_type(research_type: str):
        result = await db.execute(select(Workflow).filter(Workflow.type == research_type))
        return result.scalars().all()

    @staticmethod
    async def get_workflow_by_id(workflow_id: str):
        result = await db.execute(select(Workflow).filter(Workflow.id == workflow_id))
        return result.scalar()

    @staticmethod
    async def clear_workflow_steps(workflow_id: str):
        await db.execute(delete(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id))
        await db.commit()

        
    @staticmethod
    async def delete_process_by_id(id: str):
        try:
            await db.execute(delete(NavigationTab).where(NavigationTab.id == id))
            
            await db.commit()
            return True
        except Exception as e:
            # Log the exception or handle it accordingly
            raise e
    
    @staticmethod
    async def delete_assign_class(id: str):
        try:
            delete_query = delete(NavigationClass).where(NavigationClass.id == id)
            await db.execute(delete_query)
            await db.commit()
            return True
        except Exception as e:
            raise e
        
    @staticmethod
    async def display_process():
        query = select(NavigationTab)
        result = await db.execute(query)
        navigation_records = result.scalars().all()

        if not navigation_records:
            return []  # Return an empty list when no navigation records are found

        navigation_with_details = []
        for navigation in navigation_records:
            # Get class data
            class_query = (
                select(NavigationClass.id, NavigationClass.class_id, Class.section, Class.course)
                .join(Class, NavigationClass.class_id == Class.id)
                .where(NavigationClass.navigation_id == navigation.id)
            )
            class_data = await db.execute(class_query)
            class_data = class_data.fetchall()

            navigation_detail = {
                "id": navigation.id,
                "role": navigation.role,  # Adjust the variable name
                "type": navigation.type,
                "class_": class_data,
                "has_submitted_proposal": navigation.has_submitted_proposal,  # Adjust the variable name
                "has_pre_oral_defense_date": navigation.has_pre_oral_defense_date,
                "has_submitted_ethics_protocol": navigation.has_submitted_ethics_protocol,
                "has_submitted_full_manuscript": navigation.has_submitted_full_manuscript,
                "has_set_final_defense_date": navigation.has_set_final_defense_date,
                "has_submitted_copyright": navigation.has_submitted_copyright,
            }
            navigation_with_details.append(navigation_detail)

        return navigation_with_details
    
    
    
    @staticmethod
    async def display_process_by_type(type: str):
        query = select(NavigationTab).where(NavigationTab.type == type)
        result = await db.execute(query)
        navigation_records = result.scalars().all()

        if not navigation_records:
            return []  # Return an empty list when no navigation records are found

        navigation_with_details = []
        for navigation in navigation_records:
            # Get class data
            class_query = (
                select(NavigationClass.id, NavigationClass.class_id, Class.section, Class.course)
                .join(Class, NavigationClass.class_id == Class.id)
                .where(NavigationClass.navigation_id == navigation.id)
            )
            class_data = await db.execute(class_query)
            class_data = class_data.fetchall()

            navigation_detail = {
                "id": navigation.id,
                "role": navigation.role,  # Adjust the variable name
                "type": navigation.type,
                "class_": class_data,
                "has_submitted_proposal": navigation.has_submitted_proposal,  # Adjust the variable name
                "has_pre_oral_defense_date": navigation.has_pre_oral_defense_date,
                "has_submitted_ethics_protocol": navigation.has_submitted_ethics_protocol,
                "has_submitted_full_manuscript": navigation.has_submitted_full_manuscript,
                "has_set_final_defense_date": navigation.has_set_final_defense_date,
                "has_submitted_copyright": navigation.has_submitted_copyright,
            }
            navigation_with_details.append(navigation_detail)

        return navigation_with_details

    @staticmethod
    async def get_display_process_with_info(process):
        # Fetch section and course information for each class_id
        class_info = await SectionService.what_section_course(process.class_id)

        # Convert SQLAlchemy model to Pydantic model
        display_process = NavigationProcessDisplay(
            role=process.role,
            type=process.type,
            class_id=process.class_id,
            course=class_info.course,  # Include course information
            section=class_info.section,  # Include section information
            has_submitted_proposal=process.has_submitted_proposal,
            has_pre_oral_defense_date=process.has_pre_oral_defense_date,
            has_submitted_ethics_protocol=process.has_submitted_ethics_protocol,
            has_submitted_full_manuscript=process.has_submitted_full_manuscript,
            has_set_final_defense_date=process.has_set_final_defense_date,
            has_submitted_copyright=process.has_submitted_copyright,
        )

        return display_process

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
    
    
# todo FIX

    @staticmethod
    async def get_my_workflow(user_class: str):
        query = (
            select(Workflow, Class.course, Class.section)
            .join(WorkflowClass, Workflow.id == WorkflowClass.workflow_id)
            .join(Class, WorkflowClass.class_id == Class.id)
            .where(WorkflowClass.class_id == user_class)
        )

        result = await db.execute(query)
        rows = result.mappings().all()

        if not rows:
            return []  # Return an empty list when no workflows are found

        workflows_with_steps = []
        for row in rows:
            workflow = row[Workflow]
            course = row[Class.course]
            section = row[Class.section]

            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps = await db.execute(steps_query)
            steps = steps.scalars().all()


            #todo delete this part tapos sa schema tapos yung sa baba din
            # def_query = (
            #     select(SetDefense)
            #     .join(SetDefenseClass, SetDefenseClass.set_defense_id == SetDefense.id)
            #     .where(
            #         (SetDefense.research_type == workflow.type) &
            #         (SetDefenseClass.class_id == user_class)
            #     )
            #     .select_from(SetDefense)  # Explicitly specify the left side
            # )
            # result = await db.execute(def_query)
            # defense = result.scalars().all()

            workflow_detail = WorkflowDetail(
                id=workflow.id,
                class_id=user_class,
                type=workflow.type,
                user_id=workflow.user_id,
                course=course,
                section=section,
                steps=steps,
                #defense=defense
            )
            workflows_with_steps.append(workflow_detail)

        return workflows_with_steps
    
    
    @staticmethod
    async def get_workflowdata_by_id(workflow_id: str):
        query = (
            select(Workflow)
            .where(Workflow.id == workflow_id)
        )

        result = await db.execute(query)
        workflow = result.scalar()

        if not workflow:
            return []  # Return an empty list when no workflows are found

        steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
        steps_result = await db.execute(steps_query)
        steps = steps_result.scalars().all()

        workflow_detail = WorkflowDetailSpecific(
            id=workflow.id,
            type=workflow.type,
            steps=steps
        )

        return [workflow_detail]
    
    @staticmethod
    async def get_status_of_every_step(workflow_id: str, research_paper_id: str):
        query = (
            select(Workflow)
            .where(Workflow.id == workflow_id)
        )

        result = await db.execute(query)
        workflow = result.scalar()

        if not workflow:
            return []  # Return an empty list when no workflows are found

        steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
        steps_result = await db.execute(steps_query)
        steps = steps_result.scalars().all()

        workflow_detail = WorkflowDetailWithStatus(
            id=workflow.id,
            type=workflow.type,
            steps=[]
        )

        for step in steps:
            step_name = step.name
            status = await WorkflowService.get_status_by_step_name(step_name, research_paper_id, step.id)
            step_detail = WorkflowStepDetailWithStatus(
                id=step.id,
                name=step_name,
                description=step.description,
                status=status
            )
            workflow_detail.steps.append(step_detail)

        return [workflow_detail]
    

    @staticmethod
    async def get_status_by_step_name(step_name: str, research_paper_id: str, workflowstep_id: str):
        if step_name == "Ethics":
            ethics_query = select(Ethics.status).where(
                (Ethics.workflow_step_id == workflowstep_id) &
                (Ethics.research_paper_id == research_paper_id)
            )
            ethics_status = await db.execute(ethics_query)
            return ethics_status.scalar()
        
        elif step_name == "Proposal":
            proposal_query = select(ResearchPaper.status).where(
                (ResearchPaper.workflow_step_id == workflowstep_id) &
                (ResearchPaper.id == research_paper_id)
            )
            _status = await db.execute(proposal_query)
            return _status.scalar()

        elif step_name == "CopyRight":
            copyright_query = select(CopyRight.status).where(
                (CopyRight.workflow_step_id == workflowstep_id) &
                (CopyRight.research_paper_id == research_paper_id)
            )
            copyright_status = await db.execute(copyright_query)
            return copyright_status.scalar()
        
        elif step_name == "Pre-Oral Defense":
            def_query = select(ResearchDefense).where(
                (ResearchDefense.workflow_step_id == workflowstep_id) &
                (ResearchDefense.research_paper_id == research_paper_id) & 
                (ResearchDefense.type == 'pre-oral')
            )
            status = await db.execute(def_query)
            return "Good" if status.scalar() else None
        
        elif step_name == "Full Manuscript":
            manu_query = select(FullManuscript.status).where(
                (FullManuscript.workflow_step_id == workflowstep_id) &
                (FullManuscript.research_paper_id == research_paper_id)
            )
            manu_status = await db.execute(manu_query)
            return manu_status.scalar()
        
        elif step_name == "Final Defense":
            def2_query = select(ResearchDefense).where(
                (ResearchDefense.workflow_step_id == workflowstep_id) &
                (ResearchDefense.research_paper_id == research_paper_id) & 
                (ResearchDefense.type == 'final')
            )
            status = await db.execute(def2_query)
            return "Good" if status.scalar() else None
        return None
    
    
    
    # ITO YUNG EXPERIMENTAL =================================
    @staticmethod
    async def get_all_data_related_in_research(workflow_id: str, research_paper_id: str):
        query = (
            select(Workflow)
            .where(Workflow.id == workflow_id)
        )

        result = await db.execute(query)
        workflow = result.scalar()

        if not workflow:
            return [] 

        steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
        steps_result = await db.execute(steps_query)
        steps = steps_result.scalars().all()

        workflow_detail = WorkflowResearchInfo(
            id=workflow.id,
            type=workflow.type,
            steps=[]
        )

        for step in steps:
            step_name = step.name
            info = await WorkflowService.displayinfo_from_all(step_name, research_paper_id, step.id)
            info_dict = {"whole-info": info}
            step_detail = WorkflowResearchInfoStep(
                id=step.id,
                name=step_name,
                description=step.description,
                info=info_dict
            )
            workflow_detail.steps.append(step_detail)

        return [workflow_detail]
    
    
    @staticmethod
    async def displayinfo_from_all(step_name: str, research_paper_id: str, workflowstep_id: str):
        if step_name == "Ethics":
            ethics_query = select(Ethics).where(
                (Ethics.workflow_step_id == workflowstep_id) &
                (Ethics.research_paper_id == research_paper_id)
            )
            ethics_status = await db.execute(ethics_query)
            return ethics_status.scalars().all()
        
        elif step_name == "Proposal":
            proposal_query = select(ResearchPaper).where(
                (ResearchPaper.workflow_step_id == workflowstep_id) &
                (ResearchPaper.id == research_paper_id)
            )
            _status = await db.execute(proposal_query)
            result = _status.scalars().all()
            print(result)
            return result
        
        elif step_name == "Copyright":
            copyright_query = select(CopyRight).where(
                (CopyRight.workflow_step_id == workflowstep_id) &
                (CopyRight.research_paper_id == research_paper_id)
            )
            copyright_status = await db.execute(copyright_query)
            return copyright_status.scalars().all()
        
        elif step_name == "Pre-Oral Defense":
            def_query = select(ResearchDefense).where(
                (ResearchDefense.workflow_step_id == workflowstep_id) &
                (ResearchDefense.research_paper_id == research_paper_id) & 
                (ResearchDefense.type == 'pre-oral')
            )
            status = await db.execute(def_query)
            return status.scalars().all()
        
        elif step_name == "Full Manuscript":
            manu_query = select(FullManuscript).where(
                (FullManuscript.workflow_step_id == workflowstep_id) &
                (FullManuscript.research_paper_id == research_paper_id)
            )
            manu_status = await db.execute(manu_query)
            return manu_status.scalars().all()
        
        elif step_name == "Final Defense":
            def2_query = select(ResearchDefense).where(
                (ResearchDefense.workflow_step_id == workflowstep_id) &
                (ResearchDefense.research_paper_id == research_paper_id) & 
                (ResearchDefense.type == 'final')
            )
            status = await db.execute(def2_query)
            return status.scalars().all()
        return None
    
        
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
        async with db.transaction():
            workflow = await WorkflowService.get_workflow_id(workflow_id)
            if workflow:
                # Update workflow data
                for key, value in dict(workflow_data).items():
                    setattr(workflow, key, value)

                # Get existing steps for the workflow
                existing_steps = await db.execute(select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id))
                existing_steps = existing_steps.scalars().all()

                # Create a dictionary for quick access to existing steps by ID
                existing_steps_dict = {step.id: step for step in existing_steps}

                # Update existing steps or insert new steps
                for step_data in steps_data:
                    # Check if the step ID is provided
                    if step_data.id:
                        # Update existing step
                        existing_step = existing_steps_dict.get(step_data.id)
                        if existing_step:
                            for key, value in dict(step_data).items():
                                setattr(existing_step, key, value)
                        else:
                            # Handle the case where the provided step ID does not match any existing step
                            raise HTTPException(status_code=400, detail=f"Invalid step ID: {step_data.id}")

                    else:
                        # Insert new step
                        await WorkflowService.create_workflow_step(step_data, workflow.id)

                await db.commit()
                await db.refresh(workflow)
                return workflow

            return None
#==============deleting


    @staticmethod
    async def delete_workflow_by_id(workflow_id: str):

        try:
            # Delete workflow steps
            await db.execute(delete(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id))
            await db.execute(delete(WorkflowClass).where(WorkflowClass.workflow_id == workflow_id))
                # Delete the workflow itself
            await db.execute(delete(Workflow).where(Workflow.id == workflow_id))
            return True
        except IntegrityError as integrity_error:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to delete workflow. There is a submitted record in step. Please contact the student that submitted in this step",
            )
    
    @staticmethod
    async def delete_class_id(id: str):
        await db.execute(delete(WorkflowClass).where(WorkflowClass.id == id))

        return True
    
    @staticmethod
    async def delete_workflowstep_by_id(workflow_step_id: str):
        try:
            # Delete workflow steps
            await db.execute(delete(WorkflowStep).where(WorkflowStep.id == workflow_step_id))
            return True

        except IntegrityError as integrity_error:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to delete workflow step. There is a submitted record in step. Please contact the student that submitted in this step",
            )



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
    async def get_defense_by_workflow_step_id(workflow_step_id: str, research_paper_id: str):
        defense_result = await db.execute(
            select(ResearchDefense)
            .filter(ResearchDefense.workflow_step_id == workflow_step_id)
            .filter(ResearchDefense.research_paper_id == research_paper_id)
        )
        defense = defense_result.scalars().first() # Extract the Ethics object from the ChunkedIteratorResult object
        if defense:
            return {
                "id": defense.id,
                "type": defense.letter_of_intent,
                "date": defense.urec_9
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
    
    
    
    
    #Testing here
    
    
    @staticmethod
    async def flow_2(workflow_id: str, research_paper_id: str, user_class:str):
        query = (
            select(Workflow)
            .where(Workflow.id == workflow_id)
        )

        result = await db.execute(query)
        workflow = result.scalar()

        if not workflow:
            return [] 

        steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
        steps_result = await db.execute(steps_query)
        steps = steps_result.scalars().all()


        def_query = (
                select(SetDefense)
                .join(SetDefenseClass, SetDefenseClass.set_defense_id == SetDefense.id)
                .where(
                    (SetDefense.research_type == workflow.type) &
                    (SetDefenseClass.class_id == user_class)
                )
                .select_from(SetDefense)
            )
        result = await db.execute(def_query)
        defense = result.scalars().all()

        workflow_detail = FLOW2(
            id=workflow.id,
            type=workflow.type,
            steps=[],
            set_defense=[],
        )

        for step in steps:
            step_name = step.name
            info = await WorkflowService.flow_2_holder(step_name, research_paper_id, step.id)
            info_dict = {"whole-info": info}
            step_detail = WorkflowResearchInfoStep(
                id=step.id,
                name=step_name,
                description=step.description,
                info=info_dict
            )
            workflow_detail.steps.append(step_detail)

        if defense:
            workflow_detail.set_defense = defense
        else:
            workflow_detail.set_defense = [{"message": "No defense set by professor records found."}]

        return [workflow_detail]
    
    
    @staticmethod
    async def flow_2_holder(step_name: str, research_paper_id: str, workflowstep_id: str):
        if step_name == "Ethics":
            ethics_query = select(Ethics).where(
                (Ethics.workflow_step_id == workflowstep_id) &
                (Ethics.research_paper_id == research_paper_id)
            )
            ethics_status = await db.execute(ethics_query)
            return ethics_status.scalars().all()
        
        elif step_name == "Proposal":
            proposal_query = select(ResearchPaper).where(
                (ResearchPaper.workflow_step_id == workflowstep_id) &
                (ResearchPaper.id == research_paper_id)
            )
            _status = await db.execute(proposal_query)
            result = _status.scalars().all()
            print(result)
            return result
        
        elif step_name == "Copyright":
            copyright_query = select(CopyRight).where(
                (CopyRight.workflow_step_id == workflowstep_id) &
                (CopyRight.research_paper_id == research_paper_id)
            )
            copyright_status = await db.execute(copyright_query)
            return copyright_status.scalars().all()
        
        elif step_name == "Pre-Oral Defense":
            def_query = select(ResearchDefense).where(
                (ResearchDefense.workflow_step_id == workflowstep_id) &
                (ResearchDefense.research_paper_id == research_paper_id) & 
                (ResearchDefense.type == 'pre-oral')
            )
            status = await db.execute(def_query)
            return status.scalars().all()
        
        elif step_name == "Full Manuscript":
            manu_query = select(FullManuscript).where(
                (FullManuscript.workflow_step_id == workflowstep_id) &
                (FullManuscript.research_paper_id == research_paper_id)
            )
            manu_status = await db.execute(manu_query)
            return manu_status.scalars().all()
        
        elif step_name == "Final Defense":
            def2_query = select(ResearchDefense).where(
                (ResearchDefense.workflow_step_id == workflowstep_id) &
                (ResearchDefense.research_paper_id == research_paper_id) & 
                (ResearchDefense.type == 'final')
            )
            status = await db.execute(def2_query)
            return status.scalars().all()
        return None