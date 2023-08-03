import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("task-db.db")
        self.cursor = self.con.cursor()
        
    def create_table(self):