"""
app/models/__init__.py
初始化 models 套件，並提供資料庫連線的共用函式。
"""
import sqlite3
import os

# 資料庫檔案路徑（相對於專案根目錄）
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                       'instance', 'database.db')


def get_db():
    """
    建立並回傳一個 SQLite 資料庫連線。
    row_factory 設為 sqlite3.Row，讓查詢結果可以用欄位名稱取值（如 dict）。
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    讀取 database/schema.sql 並初始化所有資料表（若不存在則建立）。
    應在 Flask app 啟動時呼叫一次。
    """
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                               'database', 'schema.sql')
    conn = get_db()
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
