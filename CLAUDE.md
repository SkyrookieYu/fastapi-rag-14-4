# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個 **FastAPI RAG 客服 API** 的教學參考專案，目前使用假資料模擬 RAG 回答與文件清單，預計後續接入真正的 RAG 引擎（如 LangChain）與向量資料庫（如 pgvector / Chroma）。此專案作為學員學習 FastAPI 分層架構的起點範例。

## 常用指令

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動開發伺服器
uvicorn app.main:app --reload

# 跑測試（重要：必須用 python3 -m，不能直接用 pytest）
python3 -m pytest -v

# 跑單一測試
python3 -m pytest tests/test_api.py::test_health -v

# Lint 檢查
ruff check .

# Docker 啟動（含 PostgreSQL）
docker compose up --build
```

## 架構與請求流程

採用 **routes → services → models** 三層分離設計：

```
HTTP Request
  → app/routes/    （處理 HTTP 層：路由、驗證、回應格式）
    → app/services/ （業務邏輯層：目前是假資料，之後替換為真正的 RAG 引擎）
      → app/models/  （Pydantic v2 資料模型：定義 request/response schema）
```

進入點為 `app/main.py`，設定值透過 `app/config.py`（pydantic-settings `BaseSettings`）從環境變數或 `.env` 載入。未來替換真正 RAG 引擎時，只需改 `app/services/rag_service.py` 這一層。

## API 端點

| Method | Path             | 說明             |
|--------|------------------|------------------|
| GET    | `/health`        | 健康檢查          |
| POST   | `/api/chat`      | RAG 問答          |
| GET    | `/api/documents` | 文件清單          |

`/api/chat` 的 request body：`{"query": "問題", "user_id": "u1"}`

## 重要慣例

- **全部 async**：所有 handler 和 service 函式皆為 `async def`
- **Pydantic v2**：request/response model 定義在 `app/models/schemas.py`
- **測試用 httpx**：使用 `ASGITransport` + `AsyncClient`（FastAPI 官方推薦），fixture 用 `@pytest_asyncio.fixture`，測試函式須加 `@pytest.mark.asyncio`
- **chat router 前綴**：`APIRouter(prefix="/api")`，新增 chat 相關端點時加在此 router

## Docker 環境

- API 服務：`python:3.12-slim`，port `8000`
- 資料庫：`postgres:16`，帳密 `postgres/postgres`，資料庫名稱 `rag`，port `5432`
- `DATABASE_URL` 預設為 `postgresql://postgres:postgres@db:5432/rag`，可透過環境變數或 `.env` 覆寫
