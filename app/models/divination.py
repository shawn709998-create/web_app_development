"""
app/models/divination.py
算命體驗與紀錄模型（Model）

資料表 lot 欄位：
    id          INTEGER  PRIMARY KEY AUTOINCREMENT
    lot_number  INTEGER  NOT NULL UNIQUE
    grade       TEXT     NOT NULL
    title       TEXT     NOT NULL
    content     TEXT     NOT NULL
    explanation TEXT     NOT NULL
    created_at  DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))

資料表 divination_history 欄位：
    id       INTEGER  PRIMARY KEY AUTOINCREMENT
    user_id  INTEGER  NOT NULL  (FK → user.id)
    lot_id   INTEGER  NOT NULL  (FK → lot.id)
    note     TEXT
    drawn_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
"""
import sqlite3
from app.models import get_db


class Lot:
    """與 lot（籤詩內容）資料表互動的靜態方法集合。"""

    @staticmethod
    def create(lot_number: int, grade: str, title: str,
               content: str, explanation: str) -> int:
        """新增一支籤詩資料（供管理員後台使用）。"""
        try:
            conn = get_db()
            cursor = conn.execute(
                """INSERT INTO lot (lot_number, grade, title, content, explanation)
                   VALUES (?, ?, ?, ?, ?)""",
                (lot_number, grade, title, content, explanation)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in Lot.create: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all() -> list:
        """取得所有籤詩，依籤號排序。"""
        try:
            conn = get_db()
            rows = conn.execute("SELECT * FROM lot ORDER BY lot_number ASC").fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in Lot.get_all: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(lot_id: int):
        """依 ID 取得單一籤詩資料。"""
        try:
            conn = get_db()
            row = conn.execute("SELECT * FROM lot WHERE id = ?", (lot_id,)).fetchone()
            return row
        except sqlite3.Error as e:
            print(f"Database error in Lot.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def draw_random():
        """隨機抽取一支籤（核心抽籤邏輯）。"""
        try:
            conn = get_db()
            row = conn.execute("SELECT * FROM lot ORDER BY RANDOM() LIMIT 1").fetchone()
            return row
        except sqlite3.Error as e:
            print(f"Database error in Lot.draw_random: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(lot_id: int, grade: str = None, title: str = None,
               content: str = None, explanation: str = None) -> bool:
        """更新籤詩內容（只更新有傳值的欄位）。"""
        fields, params = [], []
        if grade is not None: fields.append("grade = ?"); params.append(grade)
        if title is not None: fields.append("title = ?"); params.append(title)
        if content is not None: fields.append("content = ?"); params.append(content)
        if explanation is not None: fields.append("explanation = ?"); params.append(explanation)

        if not fields:
            return False

        params.append(lot_id)
        try:
            conn = get_db()
            conn.execute(f"UPDATE lot SET {', '.join(fields)} WHERE id = ?", params)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in Lot.update: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(lot_id: int) -> bool:
        """刪除指定籤詩（若有歷史紀錄引用此籤，將受限制無法刪除）。"""
        try:
            conn = get_db()
            cursor = conn.execute("DELETE FROM lot WHERE id = ?", (lot_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in Lot.delete: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()


class DivinationHistory:
    """與 divination_history（抽籤歷史紀錄）資料表互動的靜態方法集合。"""

    @staticmethod
    def create(user_id: int, lot_id: int, note: str = None) -> int:
        """新增一筆抽籤紀錄（使用者抽到籤後呼叫此方法儲存）。"""
        try:
            conn = get_db()
            cursor = conn.execute(
                "INSERT INTO divination_history (user_id, lot_id, note) VALUES (?, ?, ?)",
                (user_id, lot_id, note)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in DivinationHistory.create: {e}")
            raise
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all() -> list:
        """取得所有歷史紀錄（管理員用），依時間新到舊排序。"""
        try:
            conn = get_db()
            rows = conn.execute("SELECT * FROM divination_history ORDER BY drawn_at DESC").fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in DivinationHistory.get_all: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(history_id: int):
        """依 ID 取得單一歷史紀錄。"""
        try:
            conn = get_db()
            row = conn.execute("SELECT * FROM divination_history WHERE id = ?", (history_id,)).fetchone()
            return row
        except sqlite3.Error as e:
            print(f"Database error in DivinationHistory.get_by_id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_user(user_id: int) -> list:
        """取得指定使用者的所有抽籤歷史（含籤詩詳細資訊）。"""
        try:
            conn = get_db()
            rows = conn.execute(
                """SELECT dh.id, dh.user_id, dh.note, dh.drawn_at,
                          l.lot_number, l.grade, l.title, l.explanation
                   FROM divination_history dh
                   JOIN lot l ON dh.lot_id = l.id
                   WHERE dh.user_id = ?
                   ORDER BY dh.drawn_at DESC""",
                (user_id,)
            ).fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in DivinationHistory.get_by_user: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(history_id: int, note: str) -> bool:
        """更新歷史紀錄的備註欄位。"""
        try:
            conn = get_db()
            cursor = conn.execute(
                "UPDATE divination_history SET note = ? WHERE id = ?",
                (note, history_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in DivinationHistory.update: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(history_id: int) -> bool:
        """刪除指定的抽籤歷史紀錄。"""
        try:
            conn = get_db()
            cursor = conn.execute("DELETE FROM divination_history WHERE id = ?", (history_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in DivinationHistory.delete: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
