"""
app.py
Flask 應用程式入口點（Entry Point）

執行方式：
    開發環境：
        flask run
    或直接執行：
        python app.py

環境變數（請複製 .env.example 為 .env 並填入實際值）：
    FLASK_APP=app.py
    FLASK_DEBUG=1
    SECRET_KEY=your-secret-key-here
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
