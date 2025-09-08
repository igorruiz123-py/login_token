from PySide6.QtWidgets import  QMainWindow
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
import smtplib
from dotenv import load_dotenv
import os
from random import randint
import re
from email.message import EmailMessage
from pathlib import Path
from db import DataBase



class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.ConfigStyle()


    def ConfigStyle(self):
        self.setStyleSheet('font-size: 15px;')
        self.setFixedSize(350, 35)


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configButton()


    def configButton(self):
        font = self.font()
        font.setPixelSize(15)
        self.setFont(font)
        self.setFixedSize(250, 50)

class Message(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configEmailMessage()

    def configEmailMessage(self):
        self.setStyleSheet('''
            font-size: 15px;
            color: red''')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(20)



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ICON_PATH = Path(__name__).parent / 'files' / 'login_image.png'
        self.token = randint(1000, 9999)
        dataBase = DataBase()

        self.mainWidget = QWidget()
        self.vLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.vLayout)
        self.setCentralWidget(self.mainWidget)

        self.setWindowTitle('Login-Token')

        self.setFixedSize(450, 700)

        icon = QIcon(str(self.ICON_PATH))
        self.setWindowIcon(icon)

        display1 = Display()
        display1.setPlaceholderText('Digite seu nome')
        self.vLayout.addWidget(display1)
        self.vLayout.setAlignment(display1, Qt.AlignmentFlag.AlignHCenter)

        self.messageName = Message()
        self.messageName.setVisible(False)
        self.vLayout.addWidget(self.messageName)

        display2 = Display()
        display2.setPlaceholderText('Digite seu E-mail')
        self.vLayout.addWidget(display2)
        self.vLayout.setAlignment(display2, Qt.AlignmentFlag.AlignHCenter)

        self.messageEmail = Message()
        self.messageEmail.setVisible(False)
        self.vLayout.addWidget(self.messageEmail)

        button1 = Button('Enviar Token por E-mail')
        self.vLayout.addWidget(button1)
        self.vLayout.setAlignment(button1, Qt.AlignmentFlag.AlignHCenter)

        button1.clicked.connect(lambda: (self.validateName(display1.text()) and self.validateEmail(display2.text()) and self.sendEmail(display2.text())))

        display3 = Display()
        display3.setPlaceholderText('Digite o Token de acesso')
        self.vLayout.addWidget(display3)
        self.vLayout.setAlignment(display3, Qt.AlignmentFlag.AlignHCenter)
        display3.setEchoMode(QLineEdit.EchoMode.Password)
        
        button2 = Button('Acessar')
        self.vLayout.addWidget(button2)
        self.vLayout.setAlignment(button2, Qt.AlignmentFlag.AlignHCenter)

        button2.clicked.connect(lambda: (self.matchTokens(self.token, int(display3.text())) and dataBase.insertNameAndEmail(display1.text(), display2.text())))

        self.messageToken = Message()   
        self.messageToken.setVisible(False)
        self.vLayout.addWidget(self.messageToken)

    
    def sendEmail(self, recipient: str):
            load_dotenv()
            smtpPort = 587
            smtpServer = 'smtp.gmail.com'
            smtpEmail = os.getenv('FROM_EMAIL')
            smtpPassword = os.getenv('EMAIL_PASSWORD')

            email = EmailMessage()
            email.set_content(
                f"""
                <html>
                    <body>
                        <p>Olá,</p>
                        <p>Aqui está o seu <b>Token de acesso ao sistema</b>:</p>
                        <h2 style='color:blue;'>{self.token}</h2>
                    </body>
                </html>
                """,
                subtype='html')
            
            email['From'] = os.getenv('FROM_EMAIL')
            email['To'] = recipient
            email['Subject'] = 'Token de Acesso ao Sistema'

            with smtplib.SMTP(smtpServer, smtpPort) as server:
                server.ehlo()
                server.starttls()
                server.login(smtpEmail, smtpPassword) # type: ignore
                server.send_message(email)

    def validateName(self, name):
        try:
            nameFormat = r'^[A-Za-zÀ-ÿ]+( [A-Za-zÀ-ÿ]+)+$'  

            if not re.match(nameFormat, name):
                raise ValueError('Digite um nome inteiro válido!')
            else:
                return True
            
        except ValueError as e:
            self.messageName.setText(f'*{str(e)}')
            self.messageName.setVisible(True)
            return False

    def validateEmail(self, email):
        try:
            emailFormat = r'^[\w\.-]+@[\w\.-]+\.\w{3,}$'

            if not re.match(emailFormat, email):
                raise ValueError('E-mail inválido!')
            else:
                return True
                        
        except ValueError as e:
                self.messageEmail.setText(f'*{str(e)}')
                self.messageEmail.setVisible(True)
                return False
        
    def matchTokens(self, token1, token2):
        try:
            if token1 != token2:
                raise ValueError('Token inválido')
            else:
                return True
            
        except ValueError as e:
                self.messageToken.setText(f'*{str(e)}')
                self.messageToken.setVisible(True)
                return False