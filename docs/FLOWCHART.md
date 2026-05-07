# 讀書筆記本系統 - 流程圖 (Flowchart)

## 1. 使用者流程圖 (User Flow)

此流程圖展示了使用者在系統中的主要操作路徑，包含瀏覽書籍、新增與管理紀錄，以及搜尋與收藏功能。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 書籍列表]
    Home --> Action{選擇操作}
    
    Action -->|點擊新增按鈕| AddPage[新增書籍頁面]
    AddPage --> FillForm[填寫書名、心得、評分]
    FillForm -->|送出表單| SaveDb1[(儲存至資料庫)]
    SaveDb1 --> Home
    
    Action -->|點擊特定書籍| DetailPage[書籍詳細內容頁面]
    DetailPage --> DetailAction{進一步操作}
    DetailAction -->|編輯| EditPage[編輯書籍頁面]
    EditPage --> EditForm[修改內容] -->|送出| SaveDb2[(更新資料庫)] --> Home
    DetailAction -->|刪除| DeleteDb[(從資料庫移除)] --> Home
    
    Action -->|使用搜尋列| Search[輸入關鍵字]
    Search -->|送出搜尋| SearchResult[顯示搜尋結果列表]
    
    Action -->|點擊收藏按鈕| ToggleFav[切換收藏狀態]
    ToggleFav --> UpdateFav[(更新資料庫)] --> Home
    Action -->|篩選收藏| FavList[只顯示已收藏書籍]
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖描述了「使用者點擊新增書籍並送出表單」到「資料存入資料庫」的完整技術運作流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask (Router/Controller)
    participant Model as Book Model
    participant DB as SQLite 資料庫

    User->>Browser: 填寫新增書籍表單並點擊送出
    Browser->>Flask: POST /add 帶有表單資料 (書名, 心得, 評分)
    Flask->>Model: 呼叫 add_book(資料)
    Model->>DB: 執行 INSERT INTO books ...
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳執行結果
    Flask-->>Browser: HTTP 302 重導向到首頁 (GET /)
    Browser->>Flask: GET /
    Flask->>Model: 呼叫 get_all_books()
    Model->>DB: 執行 SELECT * FROM books
    DB-->>Model: 回傳書籍資料列表
    Model-->>Flask: 傳遞資料物件
    Flask->>Browser: 透過 Jinja2 渲染 HTML 回傳
    Browser-->>User: 顯示更新後的書籍列表
```

## 3. 功能清單對照表

本表列出了 PRD 中定義的主要功能，及其預計對應的 URL 路徑與 HTTP 方法。

| 功能描述 | HTTP 方法 | URL 路徑 | 負責動作說明 |
| -------- | --------- | -------- | ------------ |
| **首頁/書籍列表** | GET | `/` | 顯示所有書籍紀錄的清單 |
| **新增書籍頁面** | GET | `/add` | 顯示讓使用者填寫書籍資料的表單 |
| **送出新增書籍** | POST | `/add` | 接收表單資料並儲存至資料庫，完成後重導向至首頁 |
| **書籍詳細內容** | GET | `/book/<id>` | 顯示特定書籍的詳細資訊與完整心得 |
| **編輯書籍頁面** | GET | `/edit/<id>` | 顯示編輯表單，並帶入原有的書籍資料 |
| **送出編輯更新** | POST | `/edit/<id>` | 接收更新後的資料並修改資料庫，完成後重導向至首頁 |
| **刪除書籍** | POST | `/delete/<id>` | 將特定書籍從資料庫刪除，完成後重導向至首頁 |
| **搜尋書籍** | GET | `/search` | 接收 `?q=關鍵字` 參數，查詢並顯示符合條件的書籍 |
| **切換收藏狀態** | POST | `/favorite/<id>`| 將書籍的收藏狀態反轉（收藏/取消），並重導向 |
