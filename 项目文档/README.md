# 智汇大棚 · 高附加值作物数字孪生调控终端

## 前端风格选择
- **风格C：赛博黑科技风**
- 理由：数字孪生/Plant Factory 场景需要强视觉冲击与 HUD 数据看板表达，适合竞赛展示。

## 启动说明

### 1) 后端（FastAPI）

**安装依赖**（建议使用虚拟环境）：
```bash
pip install -r backend/requirements.txt
```

**启动服务**：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**健康检查**：
- `GET http://localhost:8000/health`

**核心接口**：
- `GET http://localhost:8000/api/v1/dashboard/summary`
- `GET http://localhost:8000/api/v1/dashboard/timeseries?greenhouse_id=1`
- `POST http://localhost:8000/api/v1/control/irrigate`

> 说明：当前后端为演示版，`Service` 层提供 Mock 数据流，便于竞赛演示。

### 2) 前端（Vue3 + Vite + TailwindCSS）

**安装依赖**：
```bash
npm install
```

**启动开发服务器**：
```bash
npm run dev
```

**环境变量**：
- 复制 `frontend/.env.example` 为 `frontend/.env`
- 配置：
  - `VITE_API_BASE_URL=http://localhost:8000`

### 3) 前后端联调注意事项
- **端口**：
  - 前端默认 `5173`
  - 后端默认 `8000`
- **跨域**：后端通过 `backend/.env` 的 `CORS_ORIGINS` 放行 `http://localhost:5173`
- **API 前缀**：前端默认请求 `${VITE_API_BASE_URL}/api/v1/...`

## 演示路径
- 驾驶舱：`/dashboard`
- 棚群页：`/greenhouses`

