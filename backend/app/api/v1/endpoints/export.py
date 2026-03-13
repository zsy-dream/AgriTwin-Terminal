from __future__ import annotations

import csv
import io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter()
service = DashboardService()


@router.get("/data")
async def export_data(
    greenhouse_id: Optional[int] = Query(default=None),
    format: str = Query(default="csv", pattern="^(csv|xlsx)$"),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    gh_id = greenhouse_id or 1
    ts = await service.get_timeseries(db, greenhouse_id=gh_id)
    points = ts.get("points", [])

    if format == "csv":
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=["ts", "air_temp_c", "air_humidity_pct", "soil_moisture_pct"])
        writer.writeheader()
        for p in points:
            writer.writerow(p)
        buffer.seek(0)

        filename = f"greenhouse_{gh_id}_data_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        return StreamingResponse(
            iter([buffer.getvalue().encode("utf-8")]),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    # xlsx
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "timeseries"

    ws.append(["ts", "air_temp_c", "air_humidity_pct", "soil_moisture_pct"])
    for p in points:
        ws.append([p.get("ts"), p.get("air_temp_c"), p.get("air_humidity_pct"), p.get("soil_moisture_pct")])

    out = io.BytesIO()
    wb.save(out)
    out.seek(0)

    filename = f"greenhouse_{gh_id}_data_{datetime.utcnow().strftime('%Y%m%d')}.xlsx"
    return StreamingResponse(
        out,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/history")
async def export_history():
    # 竞赛/演示：返回空历史，后续可接数据库
    return []
