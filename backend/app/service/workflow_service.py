from datetime import datetime
import uuid
from sqlalchemy import delete, join, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select
from typing import List, Optional
import uuid
from app.config import db

from sqlalchemy.orm import Session
from fastapi import HTTPException


from app.repository.workflow_repo import WorkflowRepository
from app.model.workflowprocess import Workflow
from app.model.workflowprocess import WorkflowStep
from app.schema import WorkflowCreate, WorkflowDetail, WorkflowStepCreate




class WorkflowService:

    @staticmethod
    async def create_workflow(workflow_data: WorkflowCreate, user_id: str):
        workflow_id = str(uuid.uuid4())  # Generate UUID for workflow_id
        db_workflow = Workflow(id=workflow_id, **workflow_data.dict(), user_id=user_id)
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
    

    @staticmethod
    async def get_my_workflow(user_course: str, user_section: str):

        query = (
            select(Workflow, WorkflowStep)
            .join(WorkflowStep, Workflow.id == WorkflowStep.workflow_id)
            .where(and_(Workflow.course == user_course, Workflow.year == user_section))
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

# 28914385-40fd-43f2-ad5c-898b9263f08f