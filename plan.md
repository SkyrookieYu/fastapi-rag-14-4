# FastAPI RAG 客服 API 專案計畫

## Context
建立一個 FastAPI RAG 客服 API 的初始骨架。目前先用假資料模擬 RAG 回答與文件清單，後續再接入真正的 RAG 引擎和向量資料庫。

## 專案結構

```
fastapi-rag-14-4/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app 建立、掛載 router
│   ├── config.py             # 設定（DB URL、環境變數等）
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic v2 request/response models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py         # GET /health
│   │   └── chat.py           # POST /api/chat, GET /api/documents
│   └── services/
│       ├── __init__.py
│       └── rag_service.py    # 假資料 RAG 邏輯（之後換真的）
├── tests/
│   ├── __init__.py
│   └── test_api.py           # pytest 測試 /health 和 /api/chat
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## 各檔案內容規劃

### 1. `app/config.py`
- 用 pydantic-settings 的 `BaseSettings` 讀環境變數
- 欄位：`DATABASE_URL`、`APP_NAME`、`DEBUG`

### 2. `app/models/schemas.py`
- `ChatRequest(BaseModel)`: `query: str`, `user_id: str`
- `ChatResponse(BaseModel)`: `answer: str`, `sources: list[str]`, `user_id: str`
- `Document(BaseModel)`: `id: str`, `title: str`, `content: str`
- `DocumentListResponse(BaseModel)`: `documents: list[Document]`
- `HealthResponse(BaseModel)`: `status: str`

### 3. `app/services/rag_service.py`
- `async def get_rag_answer(query: str, user_id: str) -> ChatResponse` — 回傳假資料
- `async def get_documents() -> list[Document]` — 回傳假文件清單

### 4. `app/routes/health.py`
- `GET /health` → `HealthResponse(status="ok")`

### 5. `app/routes/chat.py`
- `POST /api/chat` → 呼叫 `rag_service.get_rag_answer`
- `GET /api/documents` → 呼叫 `rag_service.get_documents`

### 6. `app/main.py`
- 建立 `FastAPI()` app
- `include_router` 掛載 health 和 chat router

### 7. `tests/test_api.py`
- 用 `httpx.ASGITransport` + `httpx.AsyncClient` 測試（FastAPI 官方推薦方式）
- 測 `GET /health` 回傳 200 + `{"status": "ok"}`
- 測 `POST /api/chat` 回傳 200 + 包含 answer 和 sources
- 測 `GET /api/documents` 回傳 200 + 包含 documents 清單

### 8. `Dockerfile`
- 基於 `python:3.12-slim`
- 複製 requirements.txt → pip install → 複製 app
- CMD: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### 9. `docker-compose.yml`
- `api` service：build context `.`，port `8000:8000`，depends_on `db`
- `db` service：`postgres:16`，環境變數設定帳密，volume 持久化

### 10. `requirements.txt`
- fastapi, uvicorn[standard], pydantic, pydantic-settings, httpx, pytest, pytest-asyncio

### 11. `.gitignore`
- Python 標準項目：`__pycache__/`, `.env`, `.venv/`, `*.pyc`, `.pytest_cache/`

## 驗證方式
1. `pip install -r requirements.txt`
2. `pytest tests/` — 全部通過
3. `uvicorn app.main:app --reload` → 手動測三個 endpoint
4. `docker compose up --build` — 容器啟動正常，API 可存取
