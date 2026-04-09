# 系統架構文件 (線上算命系統)

本文件根據產品需求文件（PRD）中的需求，規劃本專案的技術架構、資料夾結構以及各個系統元件的互動方式與職責分配。

## 1. 技術架構說明

本系統採用傳統的伺服器渲染架構（Server-Side Rendering, SSR），不採用前後端分離，確保開發快速且架構單純，適合 MVP 快速上線並降低維護成本。

### 選用技術與原因
- **後端框架：Python + Flask**
  Flask 是輕量級的後端框架，不預設綁定過多複雜功能，開發靈活。能夠快速處理 HTTP 請求並進行邏輯控制。
- **模板引擎：Jinja2**
  Flask 內建支援的模板引擎，可以用來將 Python 處理後的資料動態渲染到 HTML 頁面上，再傳回使用者的瀏覽器。
- **資料庫：SQLite**
  將資料儲存於單一文字檔案中，無需額外安裝或設定資料庫伺服器，搬移與部署都非常輕量化。

### Flask MVC 模式說明
雖然系統不完全依照傳統 MVC 框架的重度實作，但在邏輯上依循相似的職責分離：
- **Model (模型)：** 負責一切與資料庫（SQLite）溝通的操作，包含會員資料、算命紀錄、籤詩內容等增刪改查邏輯。
- **View (視圖)：** 即 Jinja2 模板（`.html` 檔），負責呈現前端畫面，包含表單輸入、算命結果顯示、香油錢捐獻介面等。
- **Controller (控制器)：** 即 Flask 的路由（Routes），負責接收使用者從瀏覽器發送的請求（如表單送出或點擊按鈕），呼叫對應的 Model 取得資料，再將資料傳遞給 View 渲染成最終畫面。

## 2. 專案資料夾結構

以下為本專案建議的目錄與檔案結構，明確劃分 Controller、Model、View 以及靜態資源：

```text
web_app_development/
├── app/
│   ├── models/            ←【Model】與資料庫互動
│   │   ├── __init__.py
│   │   ├── user.py        ← 使用者資料庫模型 (會員註冊、登入)
│   │   ├── divination.py  ← 算命體驗與紀錄模型 (籤詩、占卜紀錄)
│   │   └── donation.py    ← 香油錢紀錄模型
│   ├── routes/            ←【Controller】Flask 路由定義
│   │   ├── __init__.py
│   │   ├── auth.py        ← 註冊、登入與會員管理相關路由
│   │   ├── main.py        ← 首頁、每日運勢及靜態頁面路由
│   │   ├── divination.py  ← 抽籤、擲筊體驗、結果分享路由
│   │   └── donation.py    ← 香油錢捐獻頁面與處理路由
│   ├── templates/         ←【View】Jinja2 HTML 模板
│   │   ├── base.html      ← 全域共用佈局 (導覽列、頁尾)
│   │   ├── auth/          ← 會員相關頁面 (login.html, register.html)
│   │   ├── divination/    ← 算命相關頁面 (draw.html, result.html, history.html)
│   │   └── donation/      ← 香油錢頁面 (donate.html, success.html)
│   └── static/            ← CSS / JS 靜態資源與圖片
│       ├── css/
│       │   └── style.css  ← 全域樣式設定
│       ├── js/
│       │   └── main.js    ← 前端互動邏輯 (如擲筊動畫、分享按鈕)
│       └── images/        ← 圖片、背景及籤筒圖示
├── instance/
│   └── database.db        ← SQLite 資料庫檔案
├── docs/                  ← 專案設計文件 (PRD.md, ARCHITECTURE.md 等)
├── .env                   ← 環境變數 (秘密金鑰、資料庫路徑等)
├── requirements.txt       ← Python 相依套件清單
└── app.py                 ← Flask 應用程式入口檔案
```

## 3. 元件關係圖

以下展示使用者在瀏覽器操作時，如何與伺服器內的 Flask 各元件互動並存取資料庫：

```mermaid
flowchart TD
    Browser(使用者瀏覽器)
    SQLite[(SQLite 資料庫)]
    
    subgraph 伺服器端 (Flask App)
        Router[Flask 路由 Controller\napp/routes/]
        Model[資料庫模型 Model\napp/models/]
        Template[Jinja2 模板 View\napp/templates/]
    end

    %% 請求流向
    Browser -- "HTTP Request\n(抽籤, 登入, 捐獻)" --> Router
    Router -- "增刪改查資料\n(如查詢歷史紀錄)" --> Model
    Model -- "SQL 讀寫" --> SQLite
    SQLite -- "回傳資料" --> Model
    Model -- "回傳資料或狀態" --> Router
    
    %% 回響流向
    Router -- "傳遞資料進行渲染" --> Template
    Template -- "生成 HTML" --> Router
    Router -- "HTTP Response (HTML/頁面)" --> Browser
```

## 4. 關鍵設計決策

1. **整合式後端渲染 (Server-Side Rendering) 優先於前後端分離**
   - **原因**：考量到此系統為 MVP 版本，減少前後端分離帶來的 API 設計、CORS 設定以及在框架間維護狀態的複雜度。透過 Jinja2 集中生成頁面，能有效加快專案初期的迭代速度。

2. **按功能特性拆分路由模組 (Blueprints)**
   - **原因**：為了避免日後所有路徑擠在同一個 `app.py` 中，我們在 `app/routes/` 下以商務邏輯（例如：`auth` 會員認證、`divination` 算命邏輯、`donation` 捐款）來劃分子模組（Blueprint）。這樣分工可以提高程式碼的可讀性，也方便未來多成員協作。

3. **靜態資源集中管理**
   - **原因**：將所有的 CSS、JS 與圖片集中於 `app/static/` 資料夾中。雖然是後端渲染架構，但為了提供具有現代感、動態且美觀的線上算命體驗（如抽籤特效或視覺化回饋），我們仍預留了 `js` 與 `css` 前端客製化開發的空間。

4. **採用 SQLite 單檔資料庫**
   - **原因**：相較於建立 MySQL 或 PostgreSQL 伺服器，SQLite 只要建立一個檔案在 `instance/` 資料夾內即可使用，降低新手學習門檻、方便備份與版本控制時的排除，且完全可以滿足線上抽籤平台（主要為讀取標籤、儲存簡易文字紀錄）的資料吞吐量需求。
