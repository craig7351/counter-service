# Release Notes

## [Unreleased]

## [1.1.0] - 2025-12-16
### Changed
- **Database Path**: 將 SQLite 資料庫檔案移動至 `data/counter.db`，以支援容器化環境的持久化儲存 (Persistent Volume)。

### Deployment Notes (Zeabur)
若部署於 Zeabur，為確保每次重新部署後資料不遺失，請務必設定 **掛載硬碟 (Volume)**。

**設定步驟**:
1. 進入專案的 **硬碟 (Disk)** 設定頁面。
2. 點擊 **掛載硬碟**。
3. 輸入以下資訊：
   - **硬碟 ID**: 自訂 (例如 `data`)
   - **掛載目錄**: `/app/data` (重要！必須完全符合)
4. 儲存並重新部署服務。

---

## [1.0.0] - 2025-12-16
### Added
- 初始版本釋出。
- 實作 `POST /api/visit` 與 `GET /api/count` API。
- 實作 `GET /api/all` API 取得所有計數。
- 加入 `demo.html` 前端範例。
