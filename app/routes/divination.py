"""
app/routes/divination.py
算命體驗（抽籤 / 擲筊 / 歷史紀錄）相關路由 (Blueprint: divination，前綴 /divination)

路由清單：
    GET  /divination/draw     → draw_page()    — 抽籤 / 擲筊頁面
    POST /divination/draw     → draw()         — 處理抽籤動作
    GET  /divination/history  → history()      — 個人歷史紀錄
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

divination_bp = Blueprint('divination', __name__)


@divination_bp.route('/draw', methods=['GET'])
def draw_page():
    """
    顯示抽籤 / 擲筊互動頁面。

    Auth:
        需登入（session 中有 user_id），未登入重導向至 /auth/login

    Template:
        divination/draw.html

    Context:
        user (dict): 目前登入的使用者資訊
    """
    pass  # TODO: 實作於階段六


@divination_bp.route('/draw', methods=['POST'])
def draw():
    """
    處理使用者確認抽籤的動作，隨機取籤並儲存紀錄。

    Auth:
        需登入（session 中有 user_id），未登入重導向至 /auth/login

    Form Fields:
        note (str, optional): 使用者的問卜問題或備註

    Flow:
        1. 從 session 取得 user_id，驗證登入狀態
        2. 呼叫 Lot.draw_random() 隨機抽取一支籤
        3. 若籤詩庫為空，以 flash 通知並重導向至 /divination/draw
        4. 呼叫 DivinationHistory.create(user_id, lot.id, note) 儲存抽籤紀錄
        5. 將籤詩結果傳入模板渲染

    Template:
        divination/result.html

    Context:
        lot (sqlite3.Row): 抽到的籤詩完整資料
        history_id (int): 剛建立的歷史紀錄 ID（供分享功能使用）

    On Error:
        籤詩庫為空時：flash 提示，重導向至 /divination/draw
        未登入：重導向至 /auth/login
    """
    pass  # TODO: 實作於階段六


@divination_bp.route('/history')
def history():
    """
    顯示目前登入使用者的所有抽籤歷史紀錄。

    Auth:
        需登入（session 中有 user_id），未登入重導向至 /auth/login

    Flow:
        1. 從 session 取得 user_id，驗證登入狀態
        2. 呼叫 DivinationHistory.get_by_user(user_id) 取得所有紀錄
           （此方法已 JOIN lot 資料表，包含籤等、標題、白話解說）

    Template:
        divination/history.html

    Context:
        histories (list[sqlite3.Row]): 使用者的抽籤歷史紀錄列表（含籤詩資訊）
    """
    pass  # TODO: 實作於階段六
