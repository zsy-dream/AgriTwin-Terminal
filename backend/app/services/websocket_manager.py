from __future__ import annotations

import asyncio
import json
from typing import Dict, List, Set

from fastapi import WebSocket, WebSocketDisconnect
from loguru import logger


class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # greenhouse_id -> set of websockets
        self.greenhouse_connections: Dict[int, Set[WebSocket]] = {}
        # 全局广播连接
        self.global_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket, greenhouse_id: int = None):
        await websocket.accept()
        if greenhouse_id:
            if greenhouse_id not in self.greenhouse_connections:
                self.greenhouse_connections[greenhouse_id] = set()
            self.greenhouse_connections[greenhouse_id].add(websocket)
            logger.info(f"WebSocket connected for greenhouse {greenhouse_id}")
        else:
            self.global_connections.add(websocket)
            logger.info("WebSocket connected for global broadcast")
    
    def disconnect(self, websocket: WebSocket, greenhouse_id: int = None):
        if greenhouse_id and greenhouse_id in self.greenhouse_connections:
            self.greenhouse_connections[greenhouse_id].discard(websocket)
            if not self.greenhouse_connections[greenhouse_id]:
                del self.greenhouse_connections[greenhouse_id]
        else:
            self.global_connections.discard(websocket)
        logger.info(f"WebSocket disconnected")
    
    async def broadcast_to_greenhouse(self, greenhouse_id: int, message: dict):
        """向特定大棚的所有连接广播"""
        if greenhouse_id not in self.greenhouse_connections:
            return
        
        disconnected = []
        for connection in self.greenhouse_connections[greenhouse_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        # 清理断开的连接
        for conn in disconnected:
            self.greenhouse_connections[greenhouse_id].discard(conn)
    
    async def broadcast_global(self, message: dict):
        """全局广播"""
        disconnected = []
        for connection in self.global_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        for conn in disconnected:
            self.global_connections.discard(conn)


# 全局连接管理器实例
manager = ConnectionManager()
