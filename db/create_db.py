# create_db.py

import sqlite3

# SQLiteデータベースファイルのパス
DB_FILE = 'reservations.db'

# データベース接続とカーソル取得のヘルパー関数
def create_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # reservationsテーブルの作成（予約情報を保存するためのテーブル）
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reserved_date TEXT NOT NULL,
            reserved_time TEXT NOT NULL,
            UNIQUE(reserved_date, reserved_time)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print(f"SQLite database '{DB_FILE}' and necessary table created successfully.")
