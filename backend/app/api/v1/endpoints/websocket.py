from __future__ import annotations

import asyncio
from datetime import datetime
from random import Random

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket_manager import manager
from app.services.dashboard_service import DashboardService

router = APIRouter()
dashboard_service = DashboardService()


@router.websocket("/greenhouse/{greenhouse_id}")
async def greenhouse_websocket(websocket: WebSocket, greenhouse_id: int):
    """大棚实时数据WebSocket连接"""
    await manager.connect(websocket, greenhouse_id)
    try:
        # 发送初始数据
        summary = await dashboard_service.get_summary(None)
        if greenhouse_id in summary.latest_by_greenhouse:
            latest = summary.latest_by_greenhouse[greenhouse_id]
            await websocket.send_json({
                "type": "initial",
                "data": {
                    "greenhouse_id": greenhouse_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "readings": latest
                }
            })
        
        # 保持连接，接收客户端心跳
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                # 处理心跳
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                # 发送心跳检测
                try:
                    await websocket.send_json({"type": "heartbeat"})
                except Exception:
                    break
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket, greenhouse_id)


@router.websocket("/global")
async def global_websocket(websocket: WebSocket):
    """全局广播WebSocket连接"""
    await manager.connect(websocket)
    try:
        # 发送欢迎消息
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to global broadcast channel"
        })
        
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                try:
                    await websocket.send_json({"type": "heartbeat"})
                except Exception:
                    break
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)


# 模拟实时数据推送任务
async def broadcast_realtime_data():
    """定期广播实时数据到所有连接的客户端"""
    rnd = Random(42)
    
    while True:
        await asyncio.sleep(5)  # 每5秒推送一次
        
        try:
            summary = await dashboard_service.get_summary(None)
            
            # 为每个大棚广播数据
            for gh_id in summary.latest_by_greenhouse:
                latest = summary.latest_by_greenhouse[gh_id]
                
                # 添加微小随机波动模拟实时变化
                message = {
                    "type": "realtime_update",
                    "data": {
                        "greenhouse_id": gh_id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "readings": {
                            "air_temp_c": round(latest.air_temp_c + rnd.uniform(-0.2, 0.2), 2),
                            "air_humidity_pct": round(latest.air_humidity_pct + rnd.uniform(-1, 1), 1),
                            "soil_moisture_pct": round(latest.soil_moisture_pct + rnd.uniform(-0.5, 0.5), 1),
                            "soil_ph": round(latest.soil_ph + rnd.uniform(-0.02, 0.02), 2),
                            "soil_ec": round(latest.soil_ec + rnd.uniform(-0.02, 0.02), 2),
                        }
                    }
                }
                
                await manager.broadcast_to_greenhouse(gh_id, message)
                
        except Exception as e:
            from loguru import logger
            logger.error(f"Broadcast error: {e}")
