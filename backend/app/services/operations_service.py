from __future__ import annotations

from datetime import datetime, timedelta
from random import Random
from typing import List

from app.schemas.operations import Alert, GreenhouseStage, SOPTask, StageInfo


class OperationsService:
    def __init__(self, seed: int = 42) -> None:
        self._rnd = Random(seed)

    def get_greenhouse_stages(self, greenhouse_id: int) -> GreenhouseStage:
        """获取大棚阶段信息"""
        stages = [
            StageInfo(id=1, name="萌芽", order=1, status="completed",
                     target_temp_min=18, target_temp_max=22,
                     target_humidity_min=70, target_humidity_max=80,
                     target_soil_moisture_min=35, target_soil_moisture_max=45),
            StageInfo(id=2, name="生长期", order=2, status="active",
                     target_temp_min=20, target_temp_max=25,
                     target_humidity_min=65, target_humidity_max=75,
                     target_soil_moisture_min=30, target_soil_moisture_max=45),
            StageInfo(id=3, name="分化", order=3, status="pending",
                     target_temp_min=22, target_temp_max=26,
                     target_humidity_min=60, target_humidity_max=70,
                     target_soil_moisture_min=25, target_soil_moisture_max=40),
            StageInfo(id=4, name="膨大", order=4, status="pending",
                     target_temp_min=20, target_temp_max=24,
                     target_humidity_min=55, target_humidity_max=65,
                     target_soil_moisture_min=20, target_soil_moisture_max=35),
        ]
        current = next(s for s in stages if s.status == "active")
        return GreenhouseStage(
            greenhouse_id=greenhouse_id,
            current_stage=current,
            all_stages=stages,
            days_in_stage=self._rnd.randint(15, 45),
            estimated_days_remaining=self._rnd.randint(30, 60)
        )

    def get_alerts(self, greenhouse_id: Optional[int] = None) -> List[Alert]:
        """获取告警列表"""
        now = datetime.utcnow()
        alerts = [
            Alert(
                id="ALT001",
                greenhouse_id=3,
                level="critical",
                title="土壤水分过低",
                message="土壤水分过低 (24.1%)，已触发自动灌溉",
                ts=now - timedelta(minutes=2),
                resolved=False,
                auto_action="自动灌溉已启动"
            ),
            Alert(
                id="ALT002",
                greenhouse_id=1,
                level="warning",
                title="夜间温度波动",
                message="夜间温度波动超过阈值 (±2.5℃)",
                ts=now - timedelta(minutes=15),
                resolved=False
            ),
            Alert(
                id="ALT003",
                greenhouse_id=2,
                level="info",
                title="明日高温预警",
                message="明日预计高温，建议提前通风",
                ts=now - timedelta(hours=1),
                resolved=False
            ),
        ]
        if greenhouse_id:
            alerts = [a for a in alerts if a.greenhouse_id == greenhouse_id]
        return alerts

    def get_sop_tasks(self, greenhouse_id: Optional[int] = None) -> List[SOPTask]:
        """获取SOP任务列表"""
        tasks = [
            SOPTask(
                id="TASK001",
                greenhouse_id=1,
                title="晨检巡棚",
                description="检查1号棚各项指标是否正常",
                scheduled_time="08:00",
                status="completed",
                priority="normal",
                assignee="张师傅"
            ),
            SOPTask(
                id="TASK002",
                greenhouse_id=2,
                title="水肥配比检查",
                description="检查2号棚水肥配比是否符合标准",
                scheduled_time="10:00",
                status="in_progress",
                priority="high",
                assignee="李师傅"
            ),
            SOPTask(
                id="TASK003",
                greenhouse_id=3,
                title="PH值调节",
                description="调节3号棚土壤PH值至目标范围",
                scheduled_time="14:00",
                status="pending",
                priority="normal",
                assignee="王师傅"
            ),
            SOPTask(
                id="TASK004",
                greenhouse_id=1,
                title="夜间温度设定",
                description="设定夜间温度曲线",
                scheduled_time="18:00",
                status="pending",
                priority="low"
            ),
        ]
        if greenhouse_id:
            tasks = [t for t in tasks if t.greenhouse_id == greenhouse_id]
        return tasks

    def complete_task(self, task_id: str, notes: Optional[str] = None) -> SOPTask:
        """完成任务"""
        return SOPTask(
            id=task_id,
            greenhouse_id=1,
            title="任务",
            description="",
            scheduled_time="08:00",
            status="completed"
        )
