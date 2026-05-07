# 讀書筆記本系統 - 系統架構設計 (Architecture)

## 1. 技術架構說明
本專案採用經典的 Web MVC（Model-View-Controller）架構設計，並針對輕量級應用進行簡化。我們選用的技術棧及原因如下：

- **後端框架：Python + Flask**
  - **原因**：Flask 輕量、靈活，非常適合快速開發中小型應用程式與 MVP (最小可行產品)。
- **模板引擎：Jinja2**
  - **原因**：內建於 Flask 中，不需前後端分離即可在伺服器端將動態資料（如書名、心得、評分）渲染進 HTML 頁面，降低開發複雜度與時間成本。
- **資料庫：SQLite**
  - **原因**：不需要額外架設資料庫伺服器，資料儲存為一個本地檔案，非常適合初學者開發的輕量級讀書筆記本系統。

### Flask MVC 模式對應與職責
- **Model（模型）**：負責與 SQLite 資料庫溝通，處理「書籍」、「心得」及「收藏」的讀寫操作，並將資料庫的原始資料封裝成 Python 物件或字典。
- **View（視圖）**：即 Jinja2 HTML 模板，負責將資料動態套入 HTML 骨架中，呈現畫面給使用者（例如：新增筆記的表單頁、書籍清單頁）。
- **Controller（控制器）**：即 Flask 的路由 (Routes)。負責接收使用者的網頁請求（如點擊搜尋、送出表單），呼叫對應的 Model 取得資料，最後傳遞給 View 進行渲染並回傳給瀏覽器。

---

## 2. 專案資料夾結構

本專案採用以下結構，以維持程式碼的整潔與可維護性：

```text
APP-/
├── app/                      # 應用程式主目錄
│   ├── models/               # 資料庫模型與操作 (Model)
│   │   └── book_model.py     # 處理書籍新增、搜尋、收藏等資料庫邏輯
│   ├── routes/               # Flask 路由配置 (Controller)
│   │   └── book_routes.py    # 定義各個網址的請求處理
│   ├── templates/            # Jinja2 HTML 模板 (View)
│   │   ├── base.html         # 網頁共用版型 (包含導覽列與共用資源)
│   │   ├── index.html        # 首頁 (顯示書籍列表)
│   │   ├── add.html          # 新增/編輯書籍頁面
│   │   └── detail.html       # 顯示單一書籍詳細內容與心得的頁面
│   └── static/               # 靜態資源目錄
│       ├── css/
│       │   └── style.css     # 網頁樣式檔
│       └── js/
│           └── main.js       # 基本前端互動腳本
├── instance/                 # 存放環境設定或本地資料檔
│   └── database.db           # SQLite 資料庫檔案 (不會被提交到 Git)
├── docs/                     # 專案說明文件目錄
│   ├── PRD.md                # 需求文件
│   └── ARCHITECTURE.md       # 系統架構設計文件 (本文件)
├── app.py                    # 程式進入點，負責啟動 Flask 伺服器並載入路由
└── README.md                 # 專案介紹
```

---

## 3. 元件關係圖

以下圖表展示使用者操作時，系統各元件之間的互動流程與資料流向：

```mermaid
flowchart TD
    Browser[使用者的瀏覽器]
    
    subgraph 伺服器端 (Flask App)
        Router[Flask Route (Controller)]
        Template[Jinja2 Template (View)]
        Model[Data Model (Model)]
    end
    
    DB[(SQLite 資料庫)]

    Browser -- "1. 發送請求 (GET/POST)" --> Router
    Router -- "2. 查詢或更新資料" --> Model
    Model -- "3. 執行 SQL 指令" --> DB
    DB -- "4. 回傳資料結果" --> Model
    Model -- "5. 封裝整理為資料結構" --> Router
    Router -- "6. 傳遞資料給模板" --> Template
    Template -- "7. 渲染完成的 HTML" --> Router
    Router -- "8. 回傳完整網頁" --> Browser
```

---

## 4. 關鍵設計決策

1. **採用伺服器端渲染 (SSR) 而非前後端分離**
   - **考量點**：專案目標為 MVP 且功能著重在資料記錄與查詢。
   - **原因**：使用 Flask + Jinja2 在後端完成 HTML 渲染，可避免初期耗費時間串接前端 API 與處理狀態管理，讓開發重心集中於核心業務邏輯。

2. **將資料庫操作抽離為獨立的 Model 層**
   - **考量點**：許多初期專案會將 SQL 寫在路由中，導致 Controller 異常龐大。
   - **原因**：將與資料庫互動的邏輯獨立放在 `app/models/`，不但可以讓路由 (Routes) 保持乾淨，未來若需新增功能（如進階搜尋）也只需在 Model 中增加方法，容易維護與擴充。

3. **使用 `base.html` 實現模板繼承**
   - **考量點**：每個頁面都有共同的標題列、選單與 CSS 引用。
   - **原因**：透過 Jinja2 的 `{% extends 'base.html' %}`，將共用骨架抽離。這大幅減少了重複的程式碼，修改全站設計（如更改背景顏色或加上通用導覽列）時只需修改一個檔案。

4. **隔離本地資料庫檔案與程式碼**
   - **考量點**：開發環境與發布環境的資料不能混淆。
   - **原因**：將 SQLite 資料庫放置在 `instance/` 資料夾下，一方面方便在本地除錯與備份，另一方面也能在 `.gitignore` 排除，避免團隊成員互推覆蓋彼此測試用的資料庫。
