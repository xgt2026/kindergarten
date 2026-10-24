from db import get_db
from datetime import datetime

def list_records(date_str=None):
    conn = get_db()
    sql = """SELECT r.*, c.name AS child_name, cl.name AS class_name 
             FROM records r 
             JOIN children c ON r.child_id = c.id 
             LEFT JOIN classes cl ON c.class_id = cl.id"""
    params = []
    if date_str:
        sql += " WHERE r.record_time LIKE ?"
        params.append(f"{date_str}%")
    sql += " ORDER BY r.record_time DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows

def add_record(child_id, record_type, operator):
    conn = get_db()
    now_str = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO records (child_id, record_type, record_time, operator) VALUES (?, ?, ?, ?)",
        (child_id, record_type, now_str, operator)
    )
    conn.commit()
    conn.close()

def delete_record(record_id):
    conn = get_db()
    conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()