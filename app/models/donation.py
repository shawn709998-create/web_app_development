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
from app.models import get_db


class Donation:
    """與 donation（香油錢捐獻紀錄）資料表互動的靜態方法集合。"""

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------
    @staticmethod
    def create(amount: int, message: str = None, user_id: int = None) -> dict:
        """
        新增一筆香油錢捐獻紀錄，並自動產生唯一收據代碼。

        Args:
            amount:  捐獻金額（新台幣元，必填）
            message: 捐獻者的祝福語（可選）
            user_id: 捐獻者的會員 ID（可為 None，表示匿名）

        Returns:
            dict 包含 'id' 與 'receipt_code'，供後續跳轉感謝頁使用
        """
        receipt_code = str(uuid.uuid4()).upper()  # 例如：A3F2-... 格式的唯一識別碼
        conn = get_db()
        cursor = conn.execute(
            """INSERT INTO donation (user_id, amount, message, receipt_code)
               VALUES (?, ?, ?, ?)""",
            (user_id, amount, message, receipt_code)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return {"id": new_id, "receipt_code": receipt_code}

    # ----------------------------------------------------------
    # READ
    # ----------------------------------------------------------
    @staticmethod
    def get_all() -> list:
        """
        取得所有捐獻紀錄（管理員後台用），依捐獻時間新到舊排序。

        Returns:
            list of sqlite3.Row
        """
        conn = get_db()
        rows = conn.execute(
            "SELECT * FROM donation ORDER BY donated_at DESC"
        ).fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(donation_id: int):
        """
        依 ID 取得單一捐獻紀錄。

        Args:
            donation_id: 欲查詢的捐獻紀錄 id

        Returns:
            sqlite3.Row 或 None
        """
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM donation WHERE id = ?", (donation_id,)
        ).fetchone()
        conn.close()
        return row

    @staticmethod
    def get_by_receipt_code(receipt_code: str):
        """
        依收據代碼取得捐獻紀錄（用於感謝頁面顯示收據）。

        Args:
            receipt_code: 系統產生的唯一收據識別碼

        Returns:
            sqlite3.Row 或 None
        """
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM donation WHERE receipt_code = ?", (receipt_code,)
        ).fetchone()
        conn.close()
        return row

    @staticmethod
    def get_by_user(user_id: int) -> list:
        """
        取得指定會員的所有捐獻紀錄，依時間新到舊排序。

        Args:
            user_id: 欲查詢的會員 ID

        Returns:
            list of sqlite3.Row
        """
        conn = get_db()
        rows = conn.execute(
            "SELECT * FROM donation WHERE user_id = ? ORDER BY donated_at DESC",
            (user_id,)
        ).fetchall()
        conn.close()
        return rows

    # ----------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------
    @staticmethod
    def update(donation_id: int, message: str) -> bool:
        """
        更新捐獻紀錄的祝福語（通常不需要更新，提供以備後用）。

        Args:
            donation_id: 欲更新的紀錄 id
            message:     新的祝福語

        Returns:
            True 若更新成功，False 若找不到紀錄
        """
        conn = get_db()
        cursor = conn.execute(
            "UPDATE donation SET message = ? WHERE id = ?",
            (message, donation_id)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------
    @staticmethod
    def delete(donation_id: int) -> bool:
        """
        刪除指定捐獻紀錄（管理員功能）。

        Args:
            donation_id: 欲刪除的紀錄 id

        Returns:
            True 若刪除成功，False 若找不到紀錄
        """
        conn = get_db()
        cursor = conn.execute("DELETE FROM donation WHERE id = ?", (donation_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
