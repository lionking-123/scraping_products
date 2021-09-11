from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

from sicessolar import sicessolar
from plataforma import plataforma
from contas import contas

import os
import sys

# ============= Const variables define part =============

FROM_RESET, _ = loadUiType(os.path.join(
    os.path.dirname(__file__), "./UI/reset.ui"))

# ============= Worker Class for Worker Thread ============


class Worker(QObject):
    finished = pyqtSignal()
    scrap_id = 0
    user_email = ""
    user_pwd = ""

    def run(self):
        if(self.scrap_id == 1):
            sicessolar(self.user_email, self.user_pwd)
        elif(self.scrap_id == 2):
            plataforma(self.user_email, self.user_pwd)
        elif(self.scrap_id == 3):
            contas(self.user_email, self.user_pwd)

        self.finished.emit()

# ============= Const variables define part =============


class MainWindow(QMainWindow, FROM_RESET):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)

        px = QPixmap("./images/back.png")
        px = px.scaled(self.back.size(), Qt.IgnoreAspectRatio)
        self.back.setPixmap(px)

        self.setWindowIcon(QIcon('./images/icon.png'))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.iconLabel.setPixmap(QPixmap("./images/icon.png"))
        self.btnMinimize.setIcon(
            QIcon(QPixmap("./images/icon_window_minimize.png")))
        self.btnClose.setIcon(QIcon(QPixmap("./images/icon_window_close.png")))

        self.btnClose.clicked.connect(self.close)
        self.btnMinimize.clicked.connect(self.showMinimized)
        self.attach_btn1.clicked.connect(self.scrape_sicessolar)
        self.attach_btn2.clicked.connect(self.scrape_plataforma)
        self.attach_btn3.clicked.connect(self.scrape_contas)

    def scrape_contas(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.scrap_id = 3
        self.worker.user_email = self.email3.text()
        self.worker.user_pwd = self.pwd3.text()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.attach_btn1.setEnabled(False)
        self.attach_btn2.setEnabled(False)
        self.attach_btn3.setEnabled(False)
        self.attach_btn4.setEnabled(False)
        self.attach_btn5.setEnabled(False)
        self.attach_btn6.setEnabled(False)
        self.attach_btn7.setEnabled(False)
        self.attach_btn3.setText("Extracting ...")

        self.thread.finished.connect(
            lambda: (self.attach_btn1.setEnabled(True),
                     self.attach_btn2.setEnabled(True),
                     self.attach_btn3.setEnabled(True),
                     self.attach_btn4.setEnabled(True),
                     self.attach_btn5.setEnabled(True),
                     self.attach_btn6.setEnabled(True),
                     self.attach_btn7.setEnabled(True),
                     self.attach_btn3.setText("Extract"))
        )

    def scrape_plataforma(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.scrap_id = 2
        self.worker.user_email = self.email2.text()
        self.worker.user_pwd = self.pwd2.text()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.attach_btn1.setEnabled(False)
        self.attach_btn2.setEnabled(False)
        self.attach_btn3.setEnabled(False)
        self.attach_btn4.setEnabled(False)
        self.attach_btn5.setEnabled(False)
        self.attach_btn6.setEnabled(False)
        self.attach_btn7.setEnabled(False)
        self.attach_btn2.setText("Extracting ...")

        self.thread.finished.connect(
            lambda: (self.attach_btn1.setEnabled(True),
                     self.attach_btn2.setEnabled(True),
                     self.attach_btn3.setEnabled(True),
                     self.attach_btn4.setEnabled(True),
                     self.attach_btn5.setEnabled(True),
                     self.attach_btn6.setEnabled(True),
                     self.attach_btn7.setEnabled(True),
                     self.attach_btn2.setText("Extract"))
        )

    def scrape_sicessolar(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.scrap_id = 1
        self.worker.user_email = self.email1.text()
        self.worker.user_pwd = self.pwd1.text()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.attach_btn1.setEnabled(False)
        self.attach_btn2.setEnabled(False)
        self.attach_btn3.setEnabled(False)
        self.attach_btn4.setEnabled(False)
        self.attach_btn5.setEnabled(False)
        self.attach_btn6.setEnabled(False)
        self.attach_btn7.setEnabled(False)
        self.attach_btn1.setText("Extracting ...")

        self.thread.finished.connect(
            lambda: (self.attach_btn1.setEnabled(True),
                     self.attach_btn2.setEnabled(True),
                     self.attach_btn3.setEnabled(True),
                     self.attach_btn4.setEnabled(True),
                     self.attach_btn5.setEnabled(True),
                     self.attach_btn6.setEnabled(True),
                     self.attach_btn7.setEnabled(True),
                     self.attach_btn1.setText("Extract"))
        )

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Application Close', 'Are you sure you want to close the application?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.close()
        else:
            event.ignore()

# ============= Application Start Point =============


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    try:
        main()
    except Exception as why:
        print(why)
