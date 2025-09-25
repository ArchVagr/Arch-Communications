from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout,QDialog,QMessageBox,QListWidgetItem, QHBoxLayout,QListWidget,QTextEdit,QSizePolicy, QApplication,QMainWindow, QGraphicsDropShadowEffect,QFormLayout,QLineEdit,QGridLayout,QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import requests

import main


class WindowManager:
    def __init__(self):
        self.windows=[]

    def add(self,window_class):
        self.windows.append(window_class(self))

    def add_main(self,window_class,user_id):
        self.windows.append(window_class(self,user_id))

    def demonstrate(self,title):
        for window in self.windows:
            if window.windowTitle() == title:
                window.show()








class Entrance(QWidget):
    def __init__(self,manager):
        super().__init__()
        self.regime = None
        self.manager=manager

        self.setWindowTitle("Entrance")
        self.resize(1100, 700)


        self.setStyleSheet("""
            QWidget { background: #240046; }
            QLabel#title {
                color: #ffffff;
                font: 700 48px "Segoe UI";
                letter-spacing: 0.5px;
            }
            QPushButton {
                color: #ffffff;
                background: transparent;
                border: 2px solid #b57cff;
                border-radius: 10px;
                padding: 10px 24px;
                font: 600 16px "Segoe UI";
            }
            QPushButton:hover { background: rgba(181,124,255,0.12); }
            QPushButton:pressed { background: rgba(181,124,255,0.22); }
        """)


        main = QVBoxLayout(self)
        main.setContentsMargins(64, 48, 64, 64)
        main.setSpacing(28)

        main.addStretch()


        self.label = QLabel("Welcome!")
        self.label.setObjectName("title")
        self.label.setAlignment(Qt.AlignCenter)


        main.addWidget(self.label, alignment=Qt.AlignCenter)


        self.signin = QPushButton("Sign Up")
        self.registration = QPushButton("Registration")


        row = QHBoxLayout()
        row.setSpacing(16)
        row.addStretch()
        row.addWidget(self.signin)
        row.addWidget(self.registration)
        row.addStretch()
        main.addLayout(row)

        main.addStretch()


        self.signin.clicked.connect(self.sign)
        self.registration.clicked.connect(self.reg)

    def sign(self):
        self.manager.demonstrate("Sign Up")
        self.close()

    def reg(self):
        self.manager.demonstrate("Registration")
        self.close()




class Registration(QWidget):
    def __init__(self,manager):
        super().__init__()
        self.manager=manager
        self.layout = QVBoxLayout()
        self.layout.setSpacing(12)
        self.setLayout(self.layout)
        self.setWindowTitle("Registration")



        self.label = QLabel("Registration")

        self.login = QLineEdit(placeholderText="Enter your login")
        self.login.setFixedHeight(40)

        self.password = QLineEdit(placeholderText="Enter your password")
        self.password.setFixedHeight(40)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.button = QPushButton("Send")

        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addStretch(1)

        self.layout.addWidget(self.login, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addStretch(1)

        self.button.clicked.connect(self.reg)

    def reg(self):
        text = self.login.text().strip(),self.password.text().strip()
        if  text[0]=='' or text[1]=='':
            QMessageBox.warning(self, "Ошибка", "Поле обязательно для заполнения!")
        else:
            response = requests.post("http://127.0.0.1:5555/add", json={"username": text[0], "password": text[1]})
            if response.json()["status"]:
                self.close()
                self.manager.add_main(Main_App,response.json())
                self.manager.demonstrate("App")
            else:
                QMessageBox.warning(self, "Ошибка", "Имя пользователя занято!")









class SignUp(QWidget):
    def __init__(self,manager):
        super().__init__()
        self.manager = manager
        # self.showMaximized()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(12)
        self.setLayout(self.layout)



        self.setWindowTitle("Sign Up")

        self.label = QLabel("Sign Up")

        self.login = QLineEdit(placeholderText="Enter your login")
        self.login.setFixedHeight(40)

        self.password = QLineEdit(placeholderText="Enter your password")
        self.password.setFixedHeight(40)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.button = QPushButton("Send")

       
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignHCenter)


        self.layout.addStretch(1)

        self.layout.addWidget(self.login, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignHCenter)


        self.layout.addStretch(1)
        self.button.clicked.connect(self.verify)

    def verify(self):
        text = self.login.text().strip(), self.password.text().strip()
        if text[0] == '' or text[1] == '':
            QMessageBox.warning(self, "Ошибка", "Поле обязательно для заполнения!")
        else:
            response = requests.post("http://127.0.0.1:5555/signin", json={"username": text[0], "password": text[1]})
            if response.json()["status"]:
                self.close()
                self.manager.add_main(Main_App, response.json())
                self.manager.demonstrate("App")
            else:
                QMessageBox.warning(self, "Ошибка", "Имя пользователя или пароль неверный!")







class NewChat(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New chat")

        self.grid = QGridLayout()

        self.entry = QLineEdit(placeholderText="username")
        self.search_button = QPushButton("Search")
        self.users_list = QListWidget()
        self.users_list.itemClicked.connect(self.on_click)


        self.grid.addWidget(self.entry, 0, 0)
        self.grid.addWidget(self.search_button, 0, 1)
        self.grid.addWidget(self.users_list, 1, 0, 1, 2)

        self.setLayout(self.grid)

        self.search_button.clicked.connect(self.search)

    def search(self):
        self.users_list.clear()
        data=self.entry.text()

        response = requests.post(
            'http://127.0.0.1:5555/search',
            json={"query": data}
        )
        print(response.text)
        if response:
            users_list = response.json()["results"]
            for i in users_list:
                for nickname, user_id in i.items():
                    item = QListWidgetItem(nickname)
                    item.setData(Qt.UserRole, user_id)
                    self.users_list.addItem(item)
        else:
            QMessageBox.warning(self,"Ошибка",'Пользователей с таким именем нет')


    def on_click(self,it:QListWidgetItem):
        print(it.data(Qt.UserRole))

class Main_App(QWidget):
    def __init__(self,manager,user_id):
        super().__init__()

        self.manager = manager
        self.layout=QGridLayout()

        self.chat=QTextEdit()
        self.type=QLineEdit()
        self.search=QPushButton("Start New Chat")
        self.enter=QPushButton("Enter")
        self.contacts=QListWidget()

        self.setWindowTitle("App")
        self.setLayout(self.layout)


        self.layout.addWidget(self.search,0,0)
        self.layout.addWidget(self.contacts,1,0,1,1)
        self.layout.addWidget(self.chat,0,1,2,2)
        self.layout.addWidget(self.type,2,1)
        self.layout.addWidget(self.enter,2,2)

        self.contacts.setFixedWidth(200)
        self.search.setFixedWidth(200)

        self.search.clicked.connect(self.open_new)

    def open_new(self):
        mini=NewChat()
        mini.exec()


class Message(QWidget):
        def __init__(self, message: str, time: str):
            super().__init__()

            main_layout = QHBoxLayout(self)


            avatar_size = 40
            pm = QPixmap(avatar_size, avatar_size)

            profile = QLabel()
            profile.setPixmap(pm)
            main_layout.addWidget(profile, alignment=Qt.AlignTop)


            body = QVBoxLayout()
            text = QLabel(message)
            text.setWordWrap(True)

            time_label = QLabel(time)
            time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            time_label.setStyleSheet("font-size: 11px; color: gray;")

            body.addWidget(text)
            body.addWidget(time_label)
            main_layout.addLayout(body)

app=QApplication([])
window=WindowManager()
window.windows.clear()

window.add(Entrance)
window.add(SignUp)
window.add(Registration)


window.demonstrate("Entrance")

app.exec()



