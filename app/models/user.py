"""
app/models/user.py
會員資料模型（Model）— 負責與 SQLite user 資料表互動。

資料表欄位：
    id            INTEGER  PRIMARY KEY AUTOINCREMENT
    username      TEXT     NOT NULL UNIQUE
    email         TEXT     NOT NULL UNIQUE
    password_hash TEXT     NOT NULL
    created_at    DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
"""
from app.models import get_db


class User:
    """與 user 資料表互動的靜態方法集合。"""

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------
    @staticmethod
    def create(username: str, email: str, password_hash: str) -> int:
        """
        新增一筆會員資料。
        
        Args:
            username:      使用者名稱（唯一）
            email:         電子郵件（唯一，用於登入）
            password_hash: 已雜湊的密碼字串（請先在 route 層用 bcrypt 處理）

        Returns:
            新插入紀錄的 id（lastrowid）
        
        Raises:
            sqlite3.IntegrityError: 若 email 或 username 重複
        """
        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    # ----------------------------------------------------------
    # READ
    # ----------------------------------------------------------
    @staticmethod
    def get_all() -> list:
        """
        取得所有會員資料。
        
        Returns:
            list of sqlite3.Row，每筆資料可用欄位名稱存取（如 row['email']）
        """
        conn = get_db()
        rows = conn.execute("SELECT * FROM user ORDER BY created_at DESC").fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(user_id: int):
        """
        依 ID 取得單一會員資料。

        Args:
            user_id: 欲查詢的會員 id

        Returns:
            sqlite3.Row 或 None（找不到時）
        """
        conn = get_db()
        row = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return row

    @staticmethod
    def get_by_email(email: str):
        """
        依電子郵件取得單一會員資料（用於登入驗證）。

        Args:
            email: 欲查詢的電子郵件

        Returns:
            sqlite3.Row 或 None
        """
        conn = get_db()
        row = conn.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
        conn.close()
        return row

    @staticmethod
    def get_by_username(username: str):
        """
        依使用者名稱取得單一會員資料（用於名稱唯一性驗證）。

        Args:
            username: 欲查詢的使用者名稱

        Returns:
            sqlite3.Row 或 None
        """
        conn = get_db()
        row = conn.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        conn.close()
        return row

    # ----------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------
    @staticmethod
    def update(user_id: int, username: str = None, password_hash: str = None) -> bool:
        """
        更新會員的名稱或密碼（只更新有傳值的欄位）。

        Args:
            user_id:       欲更新的會員 id
            username:      新的使用者名稱（可選）
            password_hash: 新的雜湊密碼（可選）

        Returns:
            True 若有更新成功，False 若沒有任何欄位被更新
        """
        fields, params = [], []
        if username is not None:
            fields.append("username = ?")
            params.append(username)
        if password_hash is not None:
            fields.append("password_hash = ?")
            params.append(password_hash)

        if not fields:
            return False

        params.append(user_id)
        conn = get_db()
        conn.execute(f"UPDATE user SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return True

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------
    @staticmethod
    def delete(user_id: int) -> bool:
        """
        刪除指定會員（相關的 divination_history 也會被 CASCADE 刪除）。

        Args:
            user_id: 欲刪除的會員 id

        Returns:
            True 若刪除成功（rowcount > 0），否則 False
        """
        conn = get_db()
        cursor = conn.execute("DELETE FROM user WHERE id = ?", (user_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
