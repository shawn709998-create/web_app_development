"""
app/routes/donation.py
香油錢捐獻相關路由 (Blueprint: donation，前綴 /donation)
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from app.models.donation import Donation
from app.models.user import User

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/donate', methods=['GET'])
def donate_page():
    """顯示香油錢捐獻表單頁面"""
    user = None
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
    return render_template('donation/donate.html', user=user)

@donation_bp.route('/donate', methods=['POST'])
def donate():
    """處理使用者送出的香油錢捐獻表單"""
    amount_str = request.form.get('amount')
    message = request.form.get('message', '')
    
    if not amount_str:
        flash('請輸入捐獻金額！', 'error')
        return redirect(url_for('donation.donate_page'))
        
    try:
        amount = int(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash('捐獻金額必須為大於 0 的正整數！', 'error')
        return redirect(url_for('donation.donate_page'))

    # 若未登入，user_id 為 None，代表匿名捐獻
    user_id = session.get('user_id')
    
    result = Donation.create(amount, message, user_id)
    
    # 成功後導向至感謝頁面，並透過 Query Parameters 傳遞收據代碼
    return redirect(url_for('donation.success', receipt=result['receipt_code']))

@donation_bp.route('/success')
def success():
    """捐款感謝頁面，顯示數位收據資訊"""
    receipt_code = request.args.get('receipt')
    
    if not receipt_code:
        abort(404)
        
    donation = Donation.get_by_receipt_code(receipt_code)
    
    if not donation:
        abort(404) # 如果找不到對應收據號碼的紀錄，回傳 404
        
    return render_template('donation/success.html', donation=donation)
