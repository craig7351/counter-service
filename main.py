import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import List

import os

# 資料庫存放目錄
DATA_DIR = "data"
# 資料庫檔案名稱
DB_NAME = os.path.join(DATA_DIR, "counter.db")

# Pydantic 模型
class VisitRequest(BaseModel):
    url: str

class CountResponse(BaseModel):
    url: str
    count: int

# 初始化資料庫
def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS page_counts (
            url TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時執行
    init_db()
    yield
    # 關閉時執行 (如果需要)

app = FastAPI(lifespan=lifespan, title="Visitor Counter Service")

# 設定 CORS，允許所有來源存取
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有標頭
)

@app.post("/api/visit", response_model=CountResponse)
async def visit_page(request: VisitRequest):
    """
    紀錄一次頁面訪問，並回傳最新計數。
    如果頁面是第一次被訪問，會建立新的紀錄。
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # 檢查 URL 是否存在
        cursor.execute("SELECT count FROM page_counts WHERE url = ?", (request.url,))
        row = cursor.fetchone()
        
        if row:
            new_count = row[0] + 1
            cursor.execute("UPDATE page_counts SET count = ? WHERE url = ?", (new_count, request.url))
        else:
            new_count = 1
            cursor.execute("INSERT INTO page_counts (url, count) VALUES (?, ?)", (request.url, new_count))
            
        conn.commit()
        conn.close()
        return CountResponse(url=request.url, count=new_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/count", response_model=CountResponse)
async def get_count(url: str):
    """
    取得指定頁面的目前計數，不會增加計數。
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM page_counts WHERE url = ?", (url,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return CountResponse(url=url, count=row[0])
        else:
            # 如果網址沒出現過，回傳 0
            return CountResponse(url=url, count=0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/all", response_model=List[CountResponse])
async def get_all_counts():
    """
    取得所有頁面的計數列表。
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT url, count FROM page_counts")
        rows = cursor.fetchall()
        conn.close()
        
        return [CountResponse(url=row[0], count=row[1]) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
