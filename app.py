from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import uuid

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DB_FILE = 'database.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------------------
# STATIC FILES
# ----------------------------------------
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "File not found", 404

# ----------------------------------------
# ADMIN API
# ----------------------------------------
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    if admin:
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route('/api/admin/credentials', methods=['PUT'])
def update_admin_credentials():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = get_db_connection()
    conn.execute('UPDATE admin SET password = ? WHERE username = ?', (password, username))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ----------------------------------------
# STAFF API
# ----------------------------------------
@app.route('/api/staff', methods=['GET'])
def get_staff():
    conn = get_db_connection()
    staff_rows = conn.execute('SELECT * FROM staff').fetchall()
    staff_list = []
    for s in staff_rows:
        s_dict = dict(s)
        tasks = conn.execute('SELECT * FROM tasks WHERE staffId = ?', (s['id'],)).fetchall()
        s_dict['tasks'] = [dict(t) for t in tasks]
        staff_list.append(s_dict)
    conn.close()
    return jsonify(staff_list)

@app.route('/api/staff', methods=['POST'])
def add_staff():
    data = request.json
    staff_id = 'STF' + str(uuid.uuid4().hex)[:6].upper()
    conn = get_db_connection()
    conn.execute('INSERT INTO staff (id, name, role, classAssigned, passcode, isFirstLogin) VALUES (?, ?, ?, ?, ?, ?)',
                 (staff_id, data['name'], data['role'], data['classAssigned'], data['passcode'], 1))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "id": staff_id})

@app.route('/api/staff/<id>', methods=['DELETE'])
def delete_staff(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE staffId = ?', (id,))
    conn.execute('DELETE FROM staff WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/staff/login', methods=['POST'])
def staff_login():
    data = request.json
    passcode = data.get('passcode')
    conn = get_db_connection()
    staff = conn.execute('SELECT * FROM staff WHERE passcode = ?', (passcode,)).fetchone()
    conn.close()
    if staff:
        return jsonify({"success": True, "staff": dict(staff)})
    return jsonify({"success": False, "error": "Invalid passcode"}), 401

@app.route('/api/staff/<id>/passcode', methods=['PUT'])
def update_staff_passcode(id):
    data = request.json
    new_passcode = data.get('passcode')
    conn = get_db_connection()
    conn.execute('UPDATE staff SET passcode = ?, isFirstLogin = 0 WHERE id = ?', (new_passcode, id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ----------------------------------------
# TASKS API
# ----------------------------------------
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_id = 'TSK' + str(uuid.uuid4().hex)[:6].upper()
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (id, staffId, description, assignedDate, deadline, status) VALUES (?, ?, ?, ?, ?, ?)',
                 (task_id, data['staffId'], data['description'], data['assignedDate'], data['deadline'], 'pending'))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "id": task_id})

@app.route('/api/tasks/<id>/status', methods=['PUT'])
def update_task_status(id):
    data = request.json
    status = data.get('status')
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ----------------------------------------
# STUDENT API
# ----------------------------------------
@app.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    student_rows = conn.execute('SELECT * FROM students').fetchall()
    student_list = []
    for s in student_rows:
        s_dict = dict(s)
        exams = conn.execute('SELECT * FROM exams WHERE studentId = ?', (s['id'],)).fetchall()
        s_dict['exams'] = [dict(e) for e in exams]
        student_list.append(s_dict)
    conn.close()
    return jsonify(student_list)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    student_id = 'STU' + str(uuid.uuid4().hex)[:6].upper()
    passcode = data.get('passcode', '1234')
    conn = get_db_connection()
    conn.execute('INSERT INTO students (id, name, class, section, passcode, isFirstLogin) VALUES (?, ?, ?, ?, ?, ?)',
                 (student_id, data['name'], data['class'], data.get('section', 'A'), passcode, 1))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "id": student_id})

@app.route('/api/students/login', methods=['POST'])
def student_login():
    data = request.json
    student_id = data.get('studentId')
    passcode = data.get('passcode')
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ? AND passcode = ?', (student_id, passcode)).fetchone()
    conn.close()
    if student:
        return jsonify({"success": True, "student": dict(student)})
    return jsonify({"success": False, "error": "Invalid student ID or passcode"}), 401

@app.route('/api/students/<id>/passcode', methods=['PUT'])
def update_student_passcode(id):
    data = request.json
    new_passcode = data.get('passcode')
    conn = get_db_connection()
    conn.execute('UPDATE students SET passcode = ?, isFirstLogin = 0 WHERE id = ?', (new_passcode, id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/exams', methods=['POST'])
def add_exam():
    data = request.json
    exam_id = 'EXM' + str(uuid.uuid4().hex)[:6].upper()
    conn = get_db_connection()
    conn.execute('INSERT INTO exams (id, studentId, examName, subject, marksObtained, totalMarks, date) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (exam_id, data['studentId'], data['examName'], data['subject'], data['marksObtained'], data['totalMarks'], data['date']))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "id": exam_id})


if __name__ == '__main__':
    app.run(port=3000, debug=True)
