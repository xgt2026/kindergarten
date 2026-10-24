from db import get_db


def list_classes():
    conn = get_db()
    rows = conn.execute("SELECT * FROM classes ORDER BY id").fetchall()
    conn.close()
    return rows


def get_class(class_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM classes WHERE id = ?", (class_id,)).fetchone()
    conn.close()
    return row


def add_class(name, grade, teacher_name):
    conn = get_db()
    conn.execute(
        "INSERT INTO classes (name, grade, teacher_name) VALUES (?, ?, ?)",
        (name, grade, teacher_name),
    )
    conn.commit()
    conn.close()


def delete_class(class_id):
    conn = get_db()
    conn.execute("DELETE FROM classes WHERE id = ?", (class_id,))
    conn.commit()
    conn.close()