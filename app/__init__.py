"""
app/__init__.py
Flask Application Factory — 建立並設定 Flask app 實例。

使用 Application Factory 模式，讓測試與不同環境設定更容易。
"""
import os
from flask import Flask
from app.models import init_db


def create_app():
    """
    建立並回傳設定好的 Flask application 實例。

    設定內容：
        - 載入 SECRET_KEY（從環境變數，開發時有預設值）
        - 設定 SQLite 資料庫路徑
        - 呼叫 init_db() 初始化資料表
        - 註冊所有 Blueprint

    Returns:
        Flask app instance
    """
    app = Flask(__name__, instance_relative_config=True)

    # ── 基本設定 ──────────────────────────────────────────────
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # ── 確保 instance 資料夾存在 ──────────────────────────────
    os.makedirs(app.instance_path, exist_ok=True)

    # ── 初始化資料庫（建立資料表）────────────────────────────
    with app.app_context():
        init_db()

    # ── 註冊所有 Blueprint ────────────────────────────────────
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
