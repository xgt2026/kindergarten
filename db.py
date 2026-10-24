import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "kindergarten.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'parent',
        real_name TEXT,
        child_id INTEGER
    );

    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade TEXT,
        teacher_name TEXT
    );

    CREATE TABLE IF NOT EXISTS children (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT,
        birthday TEXT,
        class_id INTEGER,
        guardian TEXT,
        phone TEXT,
        allergy TEXT,
        FOREIGN KEY (class_id) REFERENCES classes(id)
    );

    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER NOT NULL,
        record_type TEXT NOT NULL,
        record_time TEXT NOT NULL,
        operator TEXT,
        FOREIGN KEY (child_id) REFERENCES children(id)
    );

    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        author TEXT
    );

    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        description TEXT,
        created_at TEXT NOT NULL,
        author TEXT,
        FOREIGN KEY (child_id) REFERENCES children(id)
    );

    -- 【新增】请假表
    CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        child_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        reason TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT '待审批', -- 待审批 / 已同意 / 已驳回
        created_at TEXT NOT NULL,
        FOREIGN KEY (child_id) REFERENCES children(id)
    );
    """)

    try:
        cur.execute("ALTER TABLE users ADD COLUMN child_id INTEGER")
    except sqlite3.OperationalError:
        pass

    from werkzeug.security import generate_password_hash
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password_hash, role, real_name) VALUES (?, ?, ?, ?)",
            ("admin", generate_password_hash("admin123"), "admin", "系统管理员"),
        )

    conn.commit()
    conn.close()