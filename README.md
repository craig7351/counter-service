# 訪客計數器服務 (Visitor Counter Service)

這是一個簡單的後端服務，提供 API 讓任何網頁都能輕鬆加入「瀏覽人數統計」功能。

## 功能特色
- **簡單易用**: 只需要呼叫 API 即可增加計數或查詢計數。
- **跨網域支援 (CORS)**: 預設允許所有來源 (`*`) 呼叫，方便前端直接使用。
- **輕量級**: 使用 Python FastAPI 與 SQLite 資料庫。

## 專案結構
- `main.py`: 後端服務主程式。
- `counter.db`: SQLite 資料庫檔案 (自動產生)。
- `demo.html`: 前端範例網頁，展示如何使用此服務。
- `requirements.txt`: 專案依賴套件列表。

## 安裝與執行

### 1. 環境設定
請確保您已安裝 Python (建議 3.9+)。

建議建立虛擬環境 (Virtual Environment) 以保持環境乾淨：

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. 安裝套件
```bash
pip install -r requirements.txt
```

### 3. 啟動服務
```bash
python main.py
```
或使用 uvicorn 指令：
```bash
uvicorn main:app --reload
```
服務將會在 `http://localhost:8000` 啟動。

---

## API 使用說明

### 1. 增加計數 (Visit)
當使用者訪問您的網頁時，呼叫此 API。

- **URL**: `/api/visit`
- **Method**: `POST`
- **Body (JSON)**:
  ```json
  {
      "url": "https://your-website.com/page1"
  }
  ```
- **Response**:
  ```json
  {
      "url": "https://your-website.com/page1",
      "count": 101
  }
  ```

### 2. 查詢計數 (Get Count)
如果您只想顯示目前人數而不增加計數 (例如用在後台顯示)。

- **URL**: `/api/count`
- **Method**: `GET`
- **Query Param**: `url`
- **Example**: `/api/count?url=https://your-website.com/page1`
- **Response**:
  ```json
  {
      "url": "https://your-website.com/page1",
      "count": 101
  }
  ```

### 3. 取得所有計數 (Get All)
取得資料庫中曾經紀錄過的所有網址與計數。

- **URL**: `/api/all`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
       "url": "https://your-website.com/page1",
       "count": 101
    },
    {
       "url": "https://your-website.com/page2",
       "count": 5
    }
  ]
  ```

---

## 線上服務使用 (Zeabur)

本服務已部署於 Zeabur，您可以直接使用以下網址，無需自己架設伺服器：

**服務網址**: `https://counter-service.zeabur.app`

### 範例：使用線上 API
將前端程式碼中的 `API_URL` 替換為線上網址即可：

```javascript
// const API_URL = "http://localhost:8000/api/visit"; // 本地測試用
const API_URL = "https://counter-service.zeabur.app/api/visit"; // 線上正式用
```

其餘參數與回傳格式皆完全相同。

---

## 前端整合範例

您可以直接參考 `demo.html`，或將以下程式碼加入您的網頁：

```html
<span id="visitor-count">載入中...</span> 人氣

<script>
    // 替換成您的後端服務網址
    const API_URL = "https://counter-service.zeabur.app/api/visit"; 
    // 您目前的網頁網址，作為識別 ID
    const PAGE_URL = window.location.href; 

    fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: PAGE_URL })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("visitor-count").innerText = data.count;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("visitor-count").innerText = "N/A";
    });
</script>
```
