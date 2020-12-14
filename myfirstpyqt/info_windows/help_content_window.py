import os
import sys
from PySide2.QtCore import QUrl
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QVBoxLayout, QWidget

class HelpContentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ayuda de la aplicación de cobro de Clean Market')
        self.navegador = QWebEngineView()
        vbox = QVBoxLayout()
        vbox.addWidget(self.navegador)
        self.setLayout(vbox)

    def display_help(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static/html/help.html'))
        local_url = QUrl.fromLocalFile(file_path)
        self.navegador.load(local_url)
        self.showMaximized()
