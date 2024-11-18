from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# SQLite path for reservations
DB_FILE = './db/reservations.db'

# 接続関数
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

# 予約可能な時間帯
AVAILABLE_TIMES = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']

# 予約済みの時間帯を取得
def get_booked_times(reserved_date):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT reserved_time FROM reservations WHERE reserved_date = ?", (reserved_date,))
    booked_times = [row['reserved_time'] for row in cur.fetchall()]
    conn.close()
    return booked_times

# 予約をデータベースに追加
def add_booking(reserved_date, reserved_time):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO reservations (reserved_date, reserved_time) VALUES (?, ?)", (reserved_date, reserved_time))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    finally:
        conn.close()

# 予約可能な週の開始日と終了日を計算
def get_reservation_week():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # 今週の月曜日
    end_of_week = start_of_week + timedelta(days=6)  # 今週の日曜日
    return start_of_week.date(), end_of_week.date()

# トップページ（予約管理）
@app.route("/")
def main_page():
    start_of_week, end_of_week = get_reservation_week()
    reserved_date = request.args.get('date', start_of_week.isoformat())
    booked_times = get_booked_times(reserved_date)
    return render_template(
        'index.html',
        available_times=AVAILABLE_TIMES,
        booked_times=booked_times,
        reserved_date=reserved_date,
        start_of_week=start_of_week,
        end_of_week=end_of_week
    )

# 予約情報を取得（API）
@app.route('/api/get_reservations', methods=['GET'])
def get_reservations():
    reserved_date = request.args.get('date')
    booked_times = get_booked_times(reserved_date)
    return jsonify(booked_times)

# 予約を処理
@app.route('/reserve', methods=['POST'])
def reserve():
    reserved_date = request.form['date']
    reserved_time = request.form['time']
    if add_booking(reserved_date, reserved_time):
        return redirect(url_for('main_page', date=reserved_date))
    else:
        return "その時間帯は既に予約されています。別の時間帯を選択してください。"

if __name__ == '__main__':
    app.run(debug=True)
