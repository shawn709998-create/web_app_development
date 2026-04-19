"""
app/routes/divination.py
算命體驗（抽籤 / 擲筊 / 歷史紀錄）相關路由 (Blueprint: divination，前綴 /divination)
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.divination import Lot, DivinationHistory

divination_bp = Blueprint('divination', __name__)

@divination_bp.route('/draw', methods=['GET'])
def draw_page():
    """顯示抽籤 / 擲筊互動頁面"""
    if 'user_id' not in session:
        flash('請先登入才能進行線上抽籤。', 'warning')
        return redirect(url_for('auth.login_page'))
    return render_template('divination/draw.html')

@divination_bp.route('/draw', methods=['POST'])
def draw():
    """處理使用者確認抽籤的動作，隨機取籤並儲存紀錄"""
    if 'user_id' not in session:
        flash('請先登入才能進行線上抽籤。', 'warning')
        return redirect(url_for('auth.login_page'))

    user_id = session['user_id']
    note = request.form.get('note', '')

    lot = Lot.draw_random()
    if not lot:
        flash('目前系統中沒有籤詩資料，請聯繫管理員！', 'error')
        return redirect(url_for('divination.draw_page'))

    # 儲存抽籤紀錄
    history_id = DivinationHistory.create(user_id, lot['id'], note)
    
    return render_template('divination/result.html', lot=lot, history_id=history_id)

@divination_bp.route('/history')
def history():
    """顯示目前登入使用者的所有抽籤歷史紀錄"""
    if 'user_id' not in session:
        flash('請先登入才能查看抽籤紀錄。', 'warning')
        return redirect(url_for('auth.login_page'))

    user_id = session['user_id']
    histories = DivinationHistory.get_by_user(user_id)

    return render_template('divination/history.html', histories=histories)
