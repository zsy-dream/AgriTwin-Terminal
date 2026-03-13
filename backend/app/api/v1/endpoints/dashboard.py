from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import DashboardService

router = APIRouter()
service = DashboardService()


@router.get("/summary", response_model=DashboardSummary)
async def get_summary(db: AsyncSession = Depends(get_db)) -> DashboardSummary:
    try:
        return await service.get_summary(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeseries")
async def get_timeseries(greenhouse_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await service.get_timeseries(db, greenhouse_id=greenhouse_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/greenhouse/{greenhouse_id}/detail")
async def get_greenhouse_detail(greenhouse_id: int, db: AsyncSession = Depends(get_db)):
    """获取大棚详细信息，包括设备状态、灌溉历史等"""
    try:
        detail = await service.get_greenhouse_detail(db, greenhouse_id)
        if not detail:
            raise HTTPException(status_code=404, detail="大棚不存在")
        return detail
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_all_alerts(db: AsyncSession = Depends(get_db)):
    """获取所有活跃告警"""
    try:
        return await service.get_all_alerts(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    """确认告警"""
    try:
        result = await service.acknowledge_alert(db, alert_id)
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
