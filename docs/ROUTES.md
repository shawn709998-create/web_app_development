# 路由設計文件 (線上算命系統)

本文件依據 PRD.md、ARCHITECTURE.md、FLOWCHART.md 與 DB_DESIGN.md，規劃所有 Flask 路由的 URL、HTTP 方法、輸入/輸出與對應的 Jinja2 模板。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | Blueprint |
|------|-----------|----------|---------|-----------|
| 首頁 / 每日運勢 | GET | `/` | `main/index.html` | `main` |
| 會員註冊頁面 | GET | `/auth/register` | `auth/register.html` | `auth` |
| 處理會員註冊 | POST | `/auth/register` | — (重導向) | `auth` |
| 會員登入頁面 | GET | `/auth/login` | `auth/login.html` | `auth` |
| 處理會員登入 | POST | `/auth/login` | — (重導向) | `auth` |
| 會員登出 | GET | `/auth/logout` | — (重導向) | `auth` |
| 抽籤 / 擲筊頁面 | GET | `/divination/draw` | `divination/draw.html` | `divination` |
| 處理抽籤動作 | POST | `/divination/draw` | `divination/result.html` | `divination` |
| 個人歷史紀錄 | GET | `/divination/history` | `divination/history.html` | `divination` |
| 香油錢捐獻頁面 | GET | `/donation/donate` | `donation/donate.html` | `donation` |
| 處理捐款表單 | POST | `/donation/donate` | — (重導向) | `donation` |
| 捐款感謝頁面 | GET | `/donation/success` | `donation/success.html` | `donation` |

---

## 2. 每個路由的詳細說明

### Blueprint: `main` (`app/routes/main.py`)

---

#### `GET /` — 首頁 / 每日運勢

- **输入**：無（若已登入則從 session 取得 `user_id`）
- **處理邏輯**：
  1. 若使用者已登入，依 `user_id` 取得會員資訊
  2. 根據當日日期計算或隨機產生每日運勢文字
- **輸出**：渲染 `main/index.html`，傳入 `user`（或 None）、`daily_fortune`
- **錯誤處理**：無特殊錯誤情境

---

### Blueprint: `auth` (`app/routes/auth.py`)

---

#### `GET /auth/register` — 顯示註冊頁面

- **輸入**：無
- **處理邏輯**：若已登入則重導向至首頁；否則渲染表單
- **輸出**：渲染 `auth/register.html`

#### `POST /auth/register` — 處理註冊送出

- **輸入（表單欄位）**：
  - `username`（必填，需唯一）
  - `email`（必填，需唯一、格式正確）
  - `password`（必填，最少 6 字元）
  - `confirm_password`（必填，需與 password 相符）
- **處理邏輯**：
  1. 驗證表單欄位（空白、格式、長度）
  2. 確認 email 與 username 未重複（`User.get_by_email`、`User.get_by_username`）
  3. 以 `bcrypt` 雜湊密碼
  4. 呼叫 `User.create()` 寫入資料庫
  5. 寫入 session，登入狀態
- **輸出**：重導向至 `/`（首頁）
- **錯誤處理**：驗證失敗時回傳 `auth/register.html` 並顯示錯誤訊息

#### `GET /auth/login` — 顯示登入頁面

- **輸入**：無
- **處理邏輯**：若已登入則重導向至首頁；否則渲染表單
- **輸出**：渲染 `auth/login.html`

#### `POST /auth/login` — 處理登入送出

- **輸入（表單欄位）**：
  - `email`（必填）
  - `password`（必填）
- **處理邏輯**：
  1. `User.get_by_email(email)` 取得會員資料
  2. 以 `bcrypt.check_password_hash` 驗證密碼
  3. 驗證成功後寫入 session（`user_id`、`username`）
- **輸出**：重導向至 `/`（首頁）
- **錯誤處理**：帳號不存在或密碼錯誤時，回傳 `auth/login.html` 並顯示錯誤訊息

#### `GET /auth/logout` — 會員登出

- **輸入**：無
- **處理邏輯**：清除 session（`session.clear()`）
- **輸出**：重導向至 `/auth/login`

---

### Blueprint: `divination` (`app/routes/divination.py`)

---

#### `GET /divination/draw` — 抽籤 / 擲筊頁面

- **輸入**：無
- **處理邏輯**：需登入（未登入重導向至 `/auth/login`）；渲染抽籤動畫頁面
- **輸出**：渲染 `divination/draw.html`

#### `POST /divination/draw` — 處理抽籤動作

- **輸入（表單欄位）**：
  - `note`（選填，使用者的問卜問題）
- **處理邏輯**：
  1. 需登入驗證（從 session 取 `user_id`）
  2. 呼叫 `Lot.draw_random()` 隨機取得一支籤
  3. 呼叫 `DivinationHistory.create(user_id, lot.id, note)` 存入紀錄
  4. 將籤詩結果傳遞給模板
- **輸出**：渲染 `divination/result.html`，傳入 `lot`、`history_id`
- **錯誤處理**：籤詩庫為空時顯示錯誤提示；未登入時重導向至登入頁

#### `GET /divination/history` — 個人抽籤歷史紀錄

- **輸入**：無（從 session 取 `user_id`）
- **處理邏輯**：
  1. 需登入驗證
  2. 呼叫 `DivinationHistory.get_by_user(user_id)` 取得所有紀錄（含籤詩 JOIN）
- **輸出**：渲染 `divination/history.html`，傳入 `histories`
- **錯誤處理**：未登入時重導向至登入頁

---

### Blueprint: `donation` (`app/routes/donation.py`)

---

#### `GET /donation/donate` — 香油錢捐獻頁面

- **輸入**：無
- **處理邏輯**：渲染捐獻表單（不需登入，支援匿名捐獻）
- **輸出**：渲染 `donation/donate.html`

#### `POST /donation/donate` — 處理捐款表單送出

- **輸入（表單欄位）**：
  - `amount`（必填，正整數，單位：元）
  - `message`（選填，祝福語）
- **處理邏輯**：
  1. 驗證 `amount` 為正整數
  2. 從 session 嘗試取得 `user_id`（未登入則為 None）
  3. 呼叫 `Donation.create(amount, message, user_id)` 存入紀錄
  4. 取得回傳的 `receipt_code`
- **輸出**：重導向至 `/donation/success?receipt=<receipt_code>`
- **錯誤處理**：金額驗證失敗時回傳表單並顯示錯誤

#### `GET /donation/success` — 捐款感謝頁面

- **輸入（URL 參數）**：`?receipt=<receipt_code>`
- **處理邏輯**：
  1. 呼叫 `Donation.get_by_receipt_code(receipt_code)` 取得捐款紀錄
  2. 若找不到則回傳 404
- **輸出**：渲染 `donation/success.html`，傳入 `donation`
- **錯誤處理**：`receipt_code` 無效時顯示 404 錯誤頁

---

## 3. Jinja2 模板清單

所有模板繼承自 `app/templates/base.html`（使用 `{% extends "base.html" %}`）。

| 模板路徑 | 說明 | 繼承 |
|---------|------|------|
| `base.html` | 全域佈局（導覽列、頁尾、CSS/JS 引入） | — |
| `main/index.html` | 首頁，顯示每日運勢與功能入口 | `base.html` |
| `auth/register.html` | 會員註冊表單 | `base.html` |
| `auth/login.html` | 會員登入表單 | `base.html` |
| `divination/draw.html` | 抽籤 / 擲筊互動頁面（含動畫） | `base.html` |
| `divination/result.html` | 抽籤結果展示（籤詩全文與白話解說） | `base.html` |
| `divination/history.html` | 個人歷史紀錄列表 | `base.html` |
| `donation/donate.html` | 香油錢捐獻表單 | `base.html` |
| `donation/success.html` | 捐款感謝頁面（含數位收據） | `base.html` |
