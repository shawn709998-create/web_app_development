"""
app/routes/main.py
首頁與每日運勢相關路由 (Blueprint: main)

路由清單：
    GET  /    → index()   — 首頁，顯示每日運勢與功能入口
"""
from flask import Blueprint, render_template, session

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    首頁 / 每日運勢頁面。

    Flow:
        1. 若使用者已登入（session 中有 user_id），取得會員資訊
        2. 根據當日日期計算或隨機產生每日運勢文字
        3. 渲染首頁模板

    Template:
        main/index.html

    Context:
        user (dict|None): 目前登入的使用者資訊，未登入時為 None
        daily_fortune (str): 每日運勢文字內容
    """
    pass  # TODO: 實作於階段六
