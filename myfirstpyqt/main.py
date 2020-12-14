# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QAction, QHBoxLayout, QPushButton, QVBoxLayout, 
    QTableView, QFrame, QLineEdit, QWidget, QLabel
    )
from PySide2.QtCore import Signal
from info_windows.help_content_window import HelpContentWindow
from models.table_model import TableModel
from windows.add_product_window import AddProductWindow

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.ventanaHelp = HelpContentWindow()
        self.ventana = AddProductWindow(self)
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        help_menu = self.menuBar.addMenu('&Ayuda')
        help_content = QAction('&Contenido',self)
        help_acerca = QAction('&Acerca de',self)
        help_menu.addAction(help_content)
        help_menu.addAction(help_acerca)
        help_content.triggered.connect(self.help_content_triggered)
        focus_in_signal = Signal()
        self.majorLayout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.table = QTableView()
        self.marco = QFrame()
        self.marco.setFrameStyle(QFrame.Box)
        self.marco.setLayout(self.layout)
        self.inputCommands = LineEdit()
        self.inputCommands.setText('Ingrese un comando')
        self.inputCommands.focus_in_signal.connect(self.focus_in_command)
        self.layout.addWidget(self.inputCommands)
        self.inputCommands.returnPressed.connect(self.command_agrega_producto)
        self.inputCommands.hide()
        self.input = QLineEdit()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.input)
        self.majorLayout.addWidget(self.marco)
        self.total = QLabel()
        self.total.setText('Total: 0.00')
        self.total.setStyleSheet("{padding:0 50; margin:0 100;}")
        self.majorLayout.addWidget(self.total)
        widget = QWidget()
        widget.setLayout(self.majorLayout)
        self.datos =[
            ['ABCZ-1234', 'Paño esponja', 130.50],
            ['XYZC-2345', 'Escoba', 140.30],
            ]
        self.datosAnexos = [
            ['ABCZ-1234', 'Paño esponja', 130.50],
            ['XYZC-2345', 'Escoba', 140.30],
            ['WXYZ-1234', 'Limpiador de pisos', 150.00],
            ['ABCD-1234', 'Bote de basura grande', 1000.00]
            ]
        self.model = TableModel(self.datos, ['SKU', 'Artículo', 'Precio'])
        self.table.setModel(self.model)
        self.table.setColumnWidth(1,315)
        self.setCentralWidget(widget)
        self.input.returnPressed.connect(self.add_datos)
        self.calculate_total()

    def help_content_triggered(self):
        self.ventanaHelp.display_help()

    def add_datos(self):
        texto = self.input.text()
        valor = self.method_in(self.datosAnexos, texto)
        if(valor is None):
            self.marco.setStyleSheet("QFrame{border: 1px solid red;}")
            self.input.setStyleSheet("border: 1px solid red;")
            self.inputCommands.setText('Ingrese un comando')
            self.inputCommands.show()
        else:
            self.marco.setStyleSheet("QFrame{border: 1px solid black;}")
            self.input.setStyleSheet("border: 1px solid black;")
            self.datos.append(valor)
            self.table.model().layoutChanged.emit()
            self.calculate_total()
            self.inputCommands.hide()

    def calculate_total(self):
        agregado = 0.0
        for dato in self.datos:
            agregado += dato[2]
        self.total.setText('Total: ' + '{:.2f}'.format(agregado))

    def method_in(self, data, text):
        for element in data:
            if element[0].casefold() == text.casefold():
                return element
        return None
        
    def focus_in_command(self):
        self.inputCommands.setText('')

    def command_agrega_producto(self):
        valor = self.elige_comando(1)
        print(valor)
        if(valor == self.inputCommands.text()):
            self.ventana.display_info()
        else:
            print('Comando incorrecto')

    def comando_agregar(self):
        return 'A'

    def elige_comando(self, argument):
        return {
            1: lambda: self.comando_agregar(),
        }.get(argument, lambda: 'Opción inválida')()

class LineEdit(QLineEdit):
    focus_in_signal = Signal()
    focus_out_signal = Signal()
    def focusInEvent(self, event):
        self.focus_in_signal.emit()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focus_out_signal.emit()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.resize(600,600)
    window.show()
    app.exec_()
