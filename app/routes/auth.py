"""
app/routes/auth.py
會員認證相關路由 (Blueprint: auth，前綴 /auth)
"""
import sqlite3
import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """顯示會員註冊頁面"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    """處理會員註冊表單送出"""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # 基本驗證
    if not username or not email or not password or not confirm_password:
        flash('請填寫所有必填欄位！', 'error')
        return render_template('auth/register.html')
    
    if len(password) < 6:
        flash('密碼長度至少需要 6 個字元！', 'error')
        return render_template('auth/register.html')
        
    if password != confirm_password:
        flash('兩次輸入的密碼不一致！', 'error')
        return render_template('auth/register.html')

    # 檢查信箱是否已註冊
    if User.get_by_email(email):
        flash('此電子郵件已被註冊！', 'error')
        return render_template('auth/register.html')
        
    # 檢查帳號名稱是否已存在
    if User.get_by_username(username):
        flash('此帳號名稱已被使用！', 'error')
        return render_template('auth/register.html')

    # 密碼雜湊
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    password_hash = hashed_bytes.decode('utf-8')

    try:
        # 新增使用者
        user_id = User.create(username, email, password_hash)
        # 註冊成功後自動登入
        session['user_id'] = user_id
        session['username'] = username
        flash('註冊成功！歡迎來到線上算命系統。', 'success')
        return redirect(url_for('main.index'))
    except sqlite3.IntegrityError:
        flash('註冊失敗，帳號或信箱可能已存在。', 'error')
        return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """顯示會員登入頁面"""
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    """處理會員登入表單送出"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('請輸入電子郵件與密碼！', 'error')
        return render_template('auth/login.html')

    user = User.get_by_email(email)
    
    # 檢查帳號是否存在且密碼正確
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        session.clear() # 清除舊 Session 防範 Session Fixation
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash(f'歡迎回來，{user["username"]}！', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('電子郵件或密碼錯誤！', 'error')
        return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """會員登出"""
    session.clear()
    flash('您已成功登出。', 'success')
    return redirect(url_for('auth.login_page'))
