"""
app/routes/auth.py
會員認證相關路由 (Blueprint: auth，前綴 /auth)

路由清單：
    GET  /auth/register  → register_page()   — 顯示註冊頁面
    POST /auth/register  → register()        — 處理註冊送出
    GET  /auth/login     → login_page()      — 顯示登入頁面
    POST /auth/login     → login()           — 處理登入送出
    GET  /auth/logout    → logout()          — 會員登出
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET'])
def register_page():
    """
    顯示會員註冊頁面。

    Flow:
        1. 若使用者已登入（session 中有 user_id），直接重導向至首頁
        2. 否則渲染註冊表單

    Template:
        auth/register.html
    """
    pass  # TODO: 實作於階段六


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    處理會員註冊表單送出。

    Form Fields:
        username (str): 使用者名稱，需唯一
        email (str): 電子郵件，需唯一且格式正確
        password (str): 密碼，最少 6 字元
        confirm_password (str): 確認密碼，需與 password 相符

    Flow:
        1. 驗證所有表單欄位（空白、格式、長度）
        2. 確認 email 與 username 未被使用（User.get_by_email / get_by_username）
        3. 以 bcrypt 雜湊密碼
        4. 呼叫 User.create() 寫入資料庫
        5. 寫入 session（user_id、username），完成自動登入
        6. 重導向至首頁

    On Error:
        驗證失敗時回傳 auth/register.html，並透過 flash 顯示錯誤訊息
    """
    pass  # TODO: 實作於階段六


@auth_bp.route('/login', methods=['GET'])
def login_page():
    """
    顯示會員登入頁面。

    Flow:
        1. 若使用者已登入，直接重導向至首頁
        2. 否則渲染登入表單

    Template:
        auth/login.html
    """
    pass  # TODO: 實作於階段六


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    處理會員登入表單送出。

    Form Fields:
        email (str): 電子郵件
        password (str): 明文密碼（驗證後不儲存）

    Flow:
        1. 用 User.get_by_email(email) 查詢帳號是否存在
        2. 以 bcrypt.check_password_hash 驗證密碼正確性
        3. 驗證成功後寫入 session（user_id、username）
        4. 重導向至首頁

    On Error:
        帳號不存在或密碼錯誤時，回傳 auth/login.html 並顯示錯誤訊息
    """
    pass  # TODO: 實作於階段六


@auth_bp.route('/logout')
def logout():
    """
    會員登出，清除所有 session 資料。

    Flow:
        1. 呼叫 session.clear()
        2. 重導向至 /auth/login

    Redirect:
        /auth/login
    """
    pass  # TODO: 實作於階段六
