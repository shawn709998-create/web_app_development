"""
app/routes/__init__.py
初始化 routes 套件，並提供 register_blueprints() 輔助函式。
在 app.py 中呼叫此函式，將所有 Blueprint 統一註冊到 Flask app。
"""
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from app.routes.divination import divination_bp
from app.routes.donation import donation_bp


def register_blueprints(app):
    """
    將所有 Blueprint 註冊到 Flask app。

    Args:
        app: Flask application instance
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,       url_prefix='/auth')
    app.register_blueprint(divination_bp, url_prefix='/divination')
    app.register_blueprint(donation_bp,   url_prefix='/donation')
