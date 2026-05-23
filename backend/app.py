from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        dbname="taskdb",
        user="postgres",
        password="postgres",
        host="postgres",
        port="5432"
    )

def init_db():
    time.sleep(3)
    try:
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ DB ready")
    except Exception as e:
        print(f"Error: {e}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM tasks ORDER BY id DESC')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('INSERT INTO tasks (title) VALUES (%s) RETURNING *', (data['title'],))
        task = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(task), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        data = request.get_json()
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('UPDATE tasks SET completed = %s WHERE id = %s RETURNING *', (data['completed'], id))
        task = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(task), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s', (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'msg': 'deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)