import sqlite3
import json

class TaskModel:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                priority TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()
    
    def get_custom_categories(self):
        result = self.conn.execute("SELECT value FROM settings WHERE key = 'custom_categories'").fetchone()
        if result:
            return json.loads(result[0])
        return []
    
    def save_custom_categories(self, categories):
        self.conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", ('custom_categories', json.dumps(categories)))
        self.conn.commit()
    
    def get_all_tasks(self, category=None, priority=None):
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        query += " ORDER BY id DESC"
        return self.conn.execute(query, params).fetchall()
    
    def add_task(self, title, description, category, priority, due_date):
        self.conn.execute("INSERT INTO tasks (title, description, category, priority, due_date) VALUES (?, ?, ?, ?, ?)", (title, description, category, priority, due_date))
        self.conn.commit()
    
    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
    
    def delete_all_tasks(self):
        self.conn.execute("DELETE FROM tasks")
        self.conn.commit()
    
    def complete_task(self, task_id):
        self.conn.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        self.conn.commit()