---
name: deploy
description: >
  部署 FastAPI 應用到 staging 或 production。
  當使用者說「部署」、「deploy」、「推上去」、「上線」時使用。
disable-model-invocation: true
argument-hint: "[staging|production]"
allowed-tools: Bash, Read
---

# 部署 FastAPI 應用

目標環境：$ARGUMENTS（如果沒指定，預設 staging）

## 環境檢查
- 當前分支：!`git branch --show-current`
- 未 commit 的變更：!`git status --short`
- Docker 狀態：!`docker compose ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null || echo "Docker 未啟動"`

## 部署流程

### 1. 前置檢查
- 確認目前在 main 或 release 分支（staging 允許任何分支）
- 確認沒有未 commit 的變更
- 如果有問題，停下來告知使用者，不要繼續

### 2. 測試
- 跑 `pytest` 確認所有測試通過
- 如果有失敗的測試，停下來告知使用者

### 3. Build
- 執行 `docker compose build`
- 確認 build 成功

### 4. 部署
- staging：`docker compose -f docker-compose.staging.yml up -d`
- production：`docker compose -f docker-compose.prod.yml up -d`

### 5. 驗證
- 呼叫 `/health` endpoint 確認服務啟動
- 如果 health check 失敗，自動 rollback 到前一個版本

### 6. 輸出摘要
報告：環境、版本（git commit hash）、部署時間、health check 結果

