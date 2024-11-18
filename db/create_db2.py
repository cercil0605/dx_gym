# create_db.py

import sqlite3

# SQLiteデータベースファイルのパス
DB_FILE = './user.db'

# データベース接続とカーソル取得のヘルパー関数
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # reservationsテーブルの作成（予約情報を保存するためのテーブル）
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            password TEXT NOT NULL,
            UNIQUE(user_id, password)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print(f"SQLite database '{DB_FILE}' and necessary table created successfully.")
