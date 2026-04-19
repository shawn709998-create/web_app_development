"""
app/models/donation.py
香油錢捐獻紀錄模型（Model）— 負責與 SQLite donation 資料表互動。

資料表欄位：
    id           INTEGER  PRIMARY KEY AUTOINCREMENT
    user_id      INTEGER  （可為 NULL，支援匿名捐獻，FK → user.id）
    amount       INTEGER  NOT NULL
    message      TEXT
    receipt_code TEXT     NOT NULL UNIQUE
    donated_at   DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
"""
import uuid
import sqlite3
from app.models import get_db


class Donation:
    """與 donation（香油錢捐獻紀錄）資料表互動的靜態方法集合。"""

    @staticmethod
    def create(amount: int, message: str = None, user_id: int = None) -> dict:
        """
        新增一筆香油錢捐獻紀錄，並自動產生唯一收據代碼。
        """
        receipt_code = str(uuid.uuid4()).upper()
        try:
            conn = get_db()
            cursor = conn.execute(
                """INSERT INTO donation (user_id, amount, message, receipt_code)
                   VALUES (?, ?, ?, ?)""",
                (user_id, amount, message, receipt_code)
            )
            conn.commit()
            return {"id": cursor.lastrowid, "receipt_code": receipt_code}
        except sqlite3.Error as e:
            print(f"Database error in Donation.create: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all() -> list:
        """取得所有捐獻紀錄（管理員後台用），依捐獻時間新到舊排序。"""
        try:
            conn = get_db()
            rows = conn.execute("SELECT * FROM donation ORDER BY donated_at DESC").fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in Donation.get_all: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(donation_id: int):
        """依 ID 取得單一捐獻紀錄。"""
        try:
            conn = get_db()
            row = conn.execute("SELECT * FROM donation WHERE id = ?", (donation_id,)).fetchone()
            return row
        except sqlite3.Error as e:
            print(f"Database error in Donation.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_receipt_code(receipt_code: str):
        """依收據代碼取得捐獻紀錄（用於感謝頁面顯示收據）。"""
        try:
            conn = get_db()
            row = conn.execute("SELECT * FROM donation WHERE receipt_code = ?", (receipt_code,)).fetchone()
            return row
        except sqlite3.Error as e:
            print(f"Database error in Donation.get_by_receipt_code: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_user(user_id: int) -> list:
        """取得指定會員的所有捐獻紀錄，依時間新到舊排序。"""
        try:
            conn = get_db()
            rows = conn.execute("SELECT * FROM donation WHERE user_id = ? ORDER BY donated_at DESC", (user_id,)).fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in Donation.get_by_user: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(donation_id: int, message: str) -> bool:
        """更新捐獻紀錄的祝福語（通常不需要更新，提供以備後用）。"""
        try:
            conn = get_db()
            cursor = conn.execute("UPDATE donation SET message = ? WHERE id = ?", (message, donation_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in Donation.update: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(donation_id: int) -> bool:
        """刪除指定捐獻紀錄（管理員功能）。"""
        try:
            conn = get_db()
            cursor = conn.execute("DELETE FROM donation WHERE id = ?", (donation_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in Donation.delete: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
