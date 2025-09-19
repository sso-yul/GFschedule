import sqlite3
import os

class Database:
    def __init__(self):
        self.db_path = 'data/schedule.db'
        self.init_db()

    def init_db(self):
        # 데이터 폴더가 없으면 생성
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT
                , date TEXT NOT NULL
                , title TEXT NOT NULL
                , description TEXT
                , image_path TEXT
                , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT
                , date TEXT NOT NULL
                , task TEXT NOT NULL
                , completed BOOLEAN DEFAULT 0
                , created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    # 일정
    def get_schedule(self, date):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM schedules WHERE date = ?', (date,))
        schedules = cursor.fetchall()
        conn.close()
        return schedules

    def get_schedule_by_id(self, schedule_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM schedules WHERE id = ?', (schedule_id,))
        schedule = cursor.fetchone()
        conn.close()
        return schedule

    def add_schedule(self, date, title, description, image_path=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO schedules (date, title, description, image_path)
                            VALUES (?, ?, ?, ?)
                       ''', (date, title, description, image_path))
        conn.commit()
        conn.close()

    def update_schedule(self, schedule_id, title, description, image_path=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE schedules
                       SET title = ?, description = ?, image_path = ?
                       WHERE id = ?
                       ''', (title, description, image_path, schedule_id))
        conn.commit()
        conn.close()

    def delete_schedule(self, schedule_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM schedules WHERE id = ?', (schedule_id))
        conn.commit()
        conn.close()

    # 투두
    def get_todos(self, date):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos WHERE date = ?', (date,))
        todos = cursor.fetchall()
        conn.close()
        return todos

    def get_todo_by_id(self, todo_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        todo = cursor.fetchone()
        conn.close()
        return todo

    def add_todo(self, date, task):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (date, task) VALUES (?, ?)', (date, task))
        conn.commit()
        conn.close()

    def update_todo(self, todo_id, task):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE todos SET task = ? WHERE id = ?', (task, todo_id))
        conn.commit()
        conn.close()

    def update_todo_status(self, todo_id, completed):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE todos SET completed = ? WHERE  id = ?', (completed, todo_id))
        conn.commit()
        conn.close()

    def delete_todo(self, todo_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id))
        conn.commit()
        conn.close()
