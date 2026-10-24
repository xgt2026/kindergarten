from db import get_db
from werkzeug.security import generate_password_hash

def list_users():
    conn = get_db()
    rows = conn.execute("SELECT id, username, role, real_name FROM users ORDER BY id").fetchall()
    conn.close()
    return rows

def add_user(username, password, role, real_name):
    conn = get_db()
    conn.execute(
        "INSERT INTO users (username, password_hash, role, real_name) VALUES (?, ?, ?, ?)",
        (username, generate_password_hash(password), role, real_name)
    )
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()