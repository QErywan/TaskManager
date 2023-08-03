import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("task-db.db")
        self.cursor = self.con.cursor()
        self.create_table()
        
    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, due_date varchar(50), completed BOOLEAN NOT NULL CHECK (completed IN (0,1)))")
        self.con.commit()
        
    def create_task(self, task, due_date):
        self.cursor.execute("INSERT INTO tasks(task, due_date, completed) VALUES(?,?,?)",(task, due_date, 0))
        self.con.commit()
        
        created_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0",(task,)).fetchall()
        return created_task[-1]
    
    def get_tasks(self):
        incompleted_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()
        completed_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
        return completed_tasks, incompleted_tasks
    
    def mark_as_completed(self, task_id):
        self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?",(task_id,))
        self.con.commit()
        
    def mark_as_incompleted(self, task_id):
        self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?",(task_id,))
        self.con.commit()
        
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?",(task_id,)).fetchall()
        return task_text[0][0]
    
    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
        self.con.commit()
        
    def close_db_connection(self):
        self.con.close()