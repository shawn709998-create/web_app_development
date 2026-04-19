"""
app/routes/donation.py
香油錢捐獻相關路由 (Blueprint: donation，前綴 /donation)

路由清單：
    GET  /donation/donate   → donate_page()  — 顯示香油錢捐獻頁面
    POST /donation/donate   → donate()       — 處理捐款表單送出
    GET  /donation/success  → success()      — 捐款感謝頁面（含數位收據）
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

donation_bp = Blueprint('donation', __name__)


@donation_bp.route('/donate', methods=['GET'])
def donate_page():
    """
    顯示香油錢捐獻表單頁面。

    Auth:
        不需要登入（支援匿名捐獻）

    Template:
        donation/donate.html

    Context:
        user (dict|None): 若已登入則帶入使用者資訊，方便表單預填；未登入為 None
    """
    pass  # TODO: 實作於階段六


@donation_bp.route('/donate', methods=['POST'])
def donate():
    """
    處理使用者送出的香油錢捐獻表單。

    Auth:
        不需要登入（user_id 若無則以 None 存入，表示匿名捐獻）

    Form Fields:
        amount (int): 捐獻金額（必填，需為正整數，單位：新台幣元）
        message (str, optional): 捐獻者的祝福語

    Flow:
        1. 從 request.form 取得 amount 與 message
        2. 驗證 amount：不可為空、必須為正整數
        3. 從 session 嘗試取得 user_id（未登入則為 None）
        4. 呼叫 Donation.create(amount, message, user_id) 儲存紀錄
        5. 取得回傳的 receipt_code
        6. 重導向至 /donation/success?receipt=<receipt_code>

    Redirect:
        /donation/success?receipt=<receipt_code>

    On Error:
        金額驗證失敗：flash 提示，回傳 donation/donate.html
    """
    pass  # TODO: 實作於階段六


@donation_bp.route('/success')
def success():
    """
    捐款感謝頁面，顯示數位收據資訊。

    Auth:
        不需要登入

    Query Parameters:
        receipt (str): 捐款收據唯一識別碼（UUID 格式）

    Flow:
        1. 從 request.args 取得 receipt_code
        2. 呼叫 Donation.get_by_receipt_code(receipt_code) 查詢捐款紀錄
        3. 若找不到紀錄，回傳 404 錯誤
        4. 渲染感謝頁面並顯示收據資訊

    Template:
        donation/success.html

    Context:
        donation (sqlite3.Row): 捐款紀錄（含金額、祝福語、收據代碼、時間）

    On Error:
        receipt_code 無效或不存在：abort(404)
    """
    pass  # TODO: 實作於階段六
