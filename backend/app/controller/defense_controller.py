
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from app.repository.auth_repo import JWTBearer, JWTRepo

from app.config import db
from app.schema import DefenseCreate, DefenseUpdate, ResponseSchema
from app.service.ethics_service import EthicsService
from app.service.defense_service import DefenseService
from app.service.workflow_service import WorkflowService

from app.model import ResearchDefense

router = APIRouter(
    prefix="/defense",
    tags=['Defense'],
    dependencies=[Depends(JWTBearer())]
)


@router.post("/post", response_model=ResearchDefense)
async def submit_def(data: DefenseCreate):
    try:
        return await DefenseService.create_defense(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



@router.get("/get_defense/")
async def get_def_by_linked_res_step(research_paper_id: str, workflowstep_id: str):
    try:
        return await DefenseService.display_by_research_step(research_paper_id, workflowstep_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.get("/defense-info/{defense_id}")
async def get_def_by_linked_res_step(defense_id: str):
    try:
        return await DefenseService.display_by_id(defense_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.put("/update/{defense_id}", response_model=ResponseSchema)
async def update_defense(
    defense_id: str,
    data: DefenseUpdate
):
    try:
        return await DefenseService.update_defense(defense_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



@router.delete("/delete/{defense_id}")
async def delete_defense(defense_id: str):
    try:
        result = await DefenseService.delete_def(defense_id)
        if result:
            return {"message": "Defense deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Defense with ID {defense_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
