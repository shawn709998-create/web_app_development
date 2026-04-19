"""
app/routes/main.py
首頁與每日運勢相關路由 (Blueprint: main)
"""
import datetime
import hashlib
from flask import Blueprint, render_template, session
from app.models.user import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁 / 每日運勢頁面"""
    user = None
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
    
    # 產生每日運勢
    # 利用今天的日期字串 + 使用者 ID（如果有）作為亂數種子，確保當天看到的運勢固定
    fortunes = [
        "今日運勢極佳，適合做重要的決定！",
        "平靜的一天，適合靜下心來沉澱自己。",
        "要注意人際關係上的小摩擦，多點包容會有好結果。",
        "財運不錯，可能會有意外的小收穫！",
        "工作或學習上會有突破，請繼續保持努力。",
        "出門在外要注意安全，行車請小心。",
        "今天是適合與家人朋友團聚的好日子。",
        "可能會遇到一些挑戰，但這是成長的絕佳機會。"
    ]
    
    today_str = datetime.date.today().isoformat()
    seed_str = today_str
    if user:
        seed_str += f"_{user['id']}"
        
    seed_hash = hashlib.md5(seed_str.encode('utf-8')).hexdigest()
    fortune_index = int(seed_hash, 16) % len(fortunes)
    
    daily_fortune = fortunes[fortune_index]
    
    return render_template('main/index.html', user=user, daily_fortune=daily_fortune)
