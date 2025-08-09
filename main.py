from app import MainWindow
from PySide6.QtWidgets import QApplication
from db import DataBase


if __name__ == '__main__':
    app = QApplication()

    dataBase = DataBase()
    
    dataBase.createTable()
    
    window = MainWindow()

    window.show()

    app.exec()
