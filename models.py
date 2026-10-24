from flask_login import UserMixin
from db import get_db

class User(UserMixin):
    def __init__(self, id, username, password_hash, role, real_name=None, child_id=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.real_name = real_name
        self.child_id = child_id

def get_user_by_id(user_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return User(row["id"], row["username"], row["password_hash"], row["role"], row["real_name"], row["child_id"])
    return None

def get_user_by_username(username):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row:
        return User(row["id"], row["username"], row["password_hash"], row["role"], row["real_name"], row["child_id"])
    return None