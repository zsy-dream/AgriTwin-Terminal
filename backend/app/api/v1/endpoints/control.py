from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.control import ControlActionResponse, IrrigateRequest
from app.services.control_service import ControlService

router = APIRouter()
service = ControlService()


@router.post("/irrigate", response_model=ControlActionResponse)
async def irrigate(req: IrrigateRequest, db: AsyncSession = Depends(get_db)) -> ControlActionResponse:
    try:
        return await service.irrigate(db, req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
