-- ============================================================
-- 線上算命系統 SQLite 建表語法
-- 檔案：database/schema.sql
-- ============================================================

-- 啟用外鍵約束（SQLite 預設關閉，需手動啟用）
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- 資料表 1：user（會員資料）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user (
    id            INTEGER  PRIMARY KEY AUTOINCREMENT,
    username      TEXT     NOT NULL UNIQUE,
    email         TEXT     NOT NULL UNIQUE,
    password_hash TEXT     NOT NULL,
    created_at    DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------
-- 資料表 2：lot（籤詩內容）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS lot (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    lot_number  INTEGER  NOT NULL UNIQUE,
    grade       TEXT     NOT NULL,  -- 上上籤 / 上籤 / 中籤 / 下籤 / 大凶籤
    title       TEXT     NOT NULL,
    content     TEXT     NOT NULL,
    explanation TEXT     NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------
-- 資料表 3：divination_history（抽籤歷史紀錄）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS divination_history (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER  NOT NULL,
    lot_id    INTEGER  NOT NULL,
    note      TEXT,
    drawn_at  DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (lot_id)  REFERENCES lot(id)  ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- 資料表 4：donation（香油錢捐獻紀錄）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS donation (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER,          -- 可為 NULL（匿名捐獻）
    amount       INTEGER  NOT NULL,
    message      TEXT,
    receipt_code TEXT     NOT NULL UNIQUE,
    donated_at   DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL
);
