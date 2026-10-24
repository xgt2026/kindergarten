from db import get_db


def list_children(keyword=None, class_id=None):
    """查儿童列表，支持按姓名模糊搜索和按班级筛选，联表带出班级名"""
    conn = get_db()
    sql = """SELECT c.*, cl.name AS class_name
             FROM children c LEFT JOIN classes cl ON c.class_id = cl.id
             WHERE 1=1"""
    params = []
    if keyword:
        sql += " AND c.name LIKE ?"
        params.append(f"%{keyword}%")
    if class_id:
        sql += " AND c.class_id = ?"
        params.append(class_id)
    sql += " ORDER BY c.id DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows


def get_child(child_id):
    """获取单个儿童信息，【关键修改】：联表带出班级名"""
    conn = get_db()
    row = conn.execute(
        """SELECT c.*, cl.name AS class_name
           FROM children c LEFT JOIN classes cl ON c.class_id = cl.id
           WHERE c.id = ?""", 
        (child_id,)
    ).fetchone()
    conn.close()
    return row


def add_child(name, gender, birthday, class_id, guardian, phone, allergy):
    conn = get_db()
    conn.execute(
        """INSERT INTO children (name, gender, birthday, class_id, guardian, phone, allergy)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (name, gender, birthday, class_id, guardian, phone, allergy),
    )
    conn.commit()
    conn.close()


def update_child(child_id, name, gender, birthday, class_id, guardian, phone, allergy):
    conn = get_db()
    conn.execute(
        """UPDATE children SET name=?, gender=?, birthday=?, class_id=?,
           guardian=?, phone=?, allergy=? WHERE id=?""",
        (name, gender, birthday, class_id, guardian, phone, allergy, child_id),
    )
    conn.commit()
    conn.close()


def delete_child(child_id):
    conn = get_db()
    conn.execute("DELETE FROM children WHERE id = ?", (child_id,))
    conn.commit()
    conn.close()