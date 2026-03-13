from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.operations import Alert, GreenhouseStage, SOPTask, TaskCompleteRequest
from app.services.operations_service import OperationsService

router = APIRouter()
service = OperationsService()


@router.get("/stages/{greenhouse_id}", response_model=GreenhouseStage)
async def get_stages(greenhouse_id: int, db: AsyncSession = Depends(get_db)) -> GreenhouseStage:
    """获取大棚阶段信息"""
    try:
        return service.get_greenhouse_stages(greenhouse_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts", response_model=List[Alert])
async def get_alerts(
    greenhouse_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
) -> List[Alert]:
    """获取告警列表"""
    try:
        return service.get_alerts(greenhouse_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks", response_model=List[SOPTask])
async def get_tasks(
    greenhouse_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
) -> List[SOPTask]:
    """获取SOP任务列表"""
    try:
        return service.get_sop_tasks(greenhouse_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/{task_id}/complete", response_model=SOPTask)
async def complete_task(
    task_id: str,
    req: TaskCompleteRequest,
    db: AsyncSession = Depends(get_db)
) -> SOPTask:
    """完成任务"""
    try:
        return service.complete_task(task_id, req.notes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
