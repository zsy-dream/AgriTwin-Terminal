from __future__ import annotations

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.control import ControlActionResponse, IrrigateRequest


class ControlService:
    async def irrigate(self, db: AsyncSession, req: IrrigateRequest) -> ControlActionResponse:
        now = datetime.utcnow()
        expected = "预计土壤含水率回升至目标区间，并抑制持续干旱风险"

        return ControlActionResponse(
            action_id=int(now.timestamp()),
            greenhouse_id=req.greenhouse_id,
            ts=now,
            action_type="irrigate",
            duration_sec=req.duration_sec,
            expected_effect=expected,
        )
