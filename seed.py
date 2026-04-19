import os
import sqlite3

def seed_db():
    print("Seeding database...")
    from app import create_app
    app = create_app()
    with app.app_context():
        from app.models import get_db
        conn = get_db()
        
        # Check if already seeded
        cursor = conn.execute("SELECT COUNT(*) FROM lot")
        if cursor.fetchone()[0] == 0:
            lots = [
                (1, '上上籤', '春風得意馬蹄疾', '春風得意馬蹄疾，一日看盡長安花。', '這是非常好的運勢，代表您近期的努力將會獲得極大的回報，凡事都能順心如意，心想事成。'),
                (2, '中籤', '柳暗花明又一村', '山重水複疑無路，柳暗花明又一村。', '目前可能遇到一些困難或停滯，但請不要灰心。只要堅持下去，轉機就在不遠處。'),
                (3, '下籤', '行船偏遇打頭風', '屋漏偏逢連夜雨，行船偏遇打頭風。', '近期運勢較為低迷，不宜做重大決定或衝動行事。建議保守應對，沉潛等待時機，多積福德。'),
                (4, '上籤', '直掛雲帆濟滄海', '長風破浪會有時，直掛雲帆濟滄海。', '您有著遠大的抱負，雖然路途遙遠，但時機已到。把握機會，勇往直前，必然能達成目標。'),
                (5, '中籤', '靜水流深', '不畏浮雲遮望眼，自緣身在最高層。', '保持內心的平靜與清明，不要被外在的雜音所干擾。您的智慧能指引您看清事物的本質。')
            ]
            conn.executemany("INSERT INTO lot (lot_number, grade, title, content, explanation) VALUES (?, ?, ?, ?, ?)", lots)
            conn.commit()
            print("Successfully inserted 5 lots.")
        else:
            print("Lots already exist, skipping seed.")
            
if __name__ == '__main__':
    seed_db()
