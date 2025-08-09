import sqlite3 as sql
from pathlib import Path

class DataBase:
    def __init__(self) -> None:
        self.DB_PATH = Path(__name__).parent / 'login_token.db'
        self.TABLE_NAME = 'users'

    def openConnection(self):
        self.connection = sql.connect(self.DB_PATH)
        self.cursor = self.connection.cursor()

    def closeConnection(self):
        self.cursor.close()
        self.connection.close()

    def createTable(self):
        self.openConnection()
        self.cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_email TEXT NOT NULL UNIQUE);
            ''')
        
        self.closeConnection()
        
    def insertNameAndEmail(self, name: str, email: str):
        try:
            self.openConnection()
            self.cursor.execute(f'''
            INSERT INTO {self.TABLE_NAME}
            (user_name, user_email)
            VALUES
            (?, ?);''', (name, email))

            self.connection.commit()
            self.closeConnection()

        except Exception:
            print('Erro ao inserir Nome e E-mail ao banco de dados')