from flask import Flask, request, jsonify, send_from_directory
import sqlite3, os
from datetime import datetime

app = Flask(__name__, static_folder='static')
DB = os.path.join(os.path.dirname(__file__), 'tasks.db')

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            due_date TEXT,
            priority TEXT DEFAULT '',
            category TEXT DEFAULT '',
            completed INTEGER DEFAULT 0,
            sort_order INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )''')
        # Add sort_order column if upgrading from older version
        try:
            db.execute('ALTER TABLE tasks ADD COLUMN sort_order INTEGER DEFAULT 0')
        except:
            pass
        db.commit()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks ORDER BY sort_order ASC, created_at DESC').fetchall()
    return jsonify([dict(t) for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    db = get_db()
    # Put new tasks at the top (lowest sort_order)
    min_order = db.execute('SELECT MIN(sort_order) FROM tasks').fetchone()[0] or 0
    cur = db.execute(
        'INSERT INTO tasks (title, description, due_date, priority, category, sort_order) VALUES (?,?,?,?,?,?)',
        (data['title'], data.get('description',''), data.get('due_date'), data.get('priority',''), data.get('category',''), min_order - 1)
    )
    db.commit()
    task = db.execute('SELECT * FROM tasks WHERE id=?', (cur.lastrowid,)).fetchone()
    return jsonify(dict(task)), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    db = get_db()
    db.execute(
        'UPDATE tasks SET title=?, description=?, due_date=?, priority=?, category=?, completed=? WHERE id=?',
        (data['title'], data.get('description',''), data.get('due_date'), data.get('priority',''), data.get('category',''), data.get('completed',0), task_id)
    )
    db.commit()
    task = db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
    return jsonify(dict(task))

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    db.commit()
    return jsonify({'deleted': task_id})

@app.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    db = get_db()
    db.execute('UPDATE tasks SET completed = NOT completed WHERE id=?', (task_id,))
    db.commit()
    task = db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
    return jsonify(dict(task))

@app.route('/api/tasks/<int:task_id>/reschedule', methods=['POST'])
def reschedule_task(task_id):
    data = request.json
    db = get_db()
    db.execute('UPDATE tasks SET due_date=? WHERE id=?', (data.get('due_date'), task_id))
    db.commit()
    task = db.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
    return jsonify(dict(task))

@app.route('/api/tasks/reorder', methods=['POST'])
def reorder_tasks():
    # Receives ordered list of ids, updates sort_order for each
    ids = request.json.get('ids', [])
    db = get_db()
    for i, task_id in enumerate(ids):
        db.execute('UPDATE tasks SET sort_order=? WHERE id=?', (i, task_id))
    db.commit()
    return jsonify({'ok': True})

if __name__ == '__main__':
    init_db()
    print('\n🌅  Daybreak is running → open http://localhost:5000\n')
    app.run(debug=False, port=5000)
