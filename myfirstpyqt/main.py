# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QAction, QHBoxLayout, QPushButton, QVBoxLayout, 
    QTableView, QFrame, QLineEdit, QWidget, QLabel
    )
from PySide2.QtCore import Signal
from info_windows.help_content_window import HelpContentWindow
from models.table_model import TableModel

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.ventanaHelp = HelpContentWindow()
        self.ventana = AddProductWindow(self)
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        helpMenu = self.menuBar.addMenu("&Ayuda")
        helpContent = QAction("&Contenido",self)
        helpAcerca = QAction("&Acerca de",self)
        helpMenu.addAction(helpContent)
        helpMenu.addAction(helpAcerca)
        helpContent.triggered.connect(self.helpContentTriggered)
        # self.windowTitleChanged.connect(self.onWindowTitleChange)
        focus_in_signal = Signal()
        self.majorLayout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.table = QTableView()
        self.marco = QFrame();
        self.marco.setFrameStyle(QFrame.Box)
        self.marco.setLayout(self.layout)
        self.inputCommands = LineEdit()
        self.inputCommands.setText("Ingrese un comando")
        self.inputCommands.focus_in_signal.connect(self.focusInCommand)
        self.layout.addWidget(self.inputCommands)
        self.inputCommands.returnPressed.connect(self.commandAgregaProducto)
        self.inputCommands.hide()
        self.input = QLineEdit()
        #self.btn = QPushButton("Agregar")
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.input)
        #self.layout.addWidget(self.btn)
        self.majorLayout.addWidget(self.marco)
        self.total = QLabel()
        self.total.setText("Total: 0.00")
        self.total.setStyleSheet("{padding:0 50; margin:0 100;}")
        self.majorLayout.addWidget(self.total)
        widget = QWidget()
        widget.setLayout(self.majorLayout)
        self.datos =[["ABCZ-1234","Paño esponja",130.50],
        ["XYZC-2345","Escoba",140.30]]
        self.datosAnexos = [["ABCZ-1234","Paño esponja",130.50],
        ["XYZC-2345","Escoba",140.30],
        ["WXYZ-1234","Limpiador de pisos",150.00],["ABCD-1234","Bote de basura grande",1000.00]]
        self.model = TableModel(self.datos, ["SKU","Artículo","Precio"])
        self.table.setModel(self.model)
        self.table.setColumnWidth(1,315)
        self.setCentralWidget(widget)
        #self.btn.clicked.connect(self.addDatos)
        self.input.returnPressed.connect(self.addDatos)
        self.calculateTotal()

    def helpContentTriggered(self):
        print("Conectado al contenido de la ayuda")
        self.ventanaHelp.display_help()

    def addDatos(self):
        texto = self.input.text()
        valor = self.method_in(self.datosAnexos,texto)
        if(valor is None):
            self.marco.setStyleSheet("QFrame{border: 1px solid red;}")
            self.input.setStyleSheet("border: 1px solid red;")
            self.inputCommands.setText("Ingrese un comando")
            self.inputCommands.show()
        else:
            self.marco.setStyleSheet("QFrame{border: 1px solid black;}")
            self.input.setStyleSheet("border: 1px solid black;")
            self.datos.append(valor)
            self.table.model().layoutChanged.emit()
            self.calculateTotal()
            self.inputCommands.hide()

    def calculateTotal(self):
        agregado = 0.0;
        for i in self.datos:
            agregado += i[2]
        valorfinal = "{:.2f}".format(agregado)
        print("el precio total es "+valorfinal)
        self.total.setText("Total: "+valorfinal)

    def method_in(self,a, b):
        for i in a:
            if i[0] == b:
                return i
        return None;
    def focusInCommand(self):
        self.inputCommands.setText("")

    def commandAgregaProducto(self):
        valor = self.eligeComando(1)
        print(valor)
        if(valor == self.inputCommands.text()):
            self.ventana.displayInfo()
        else:
            print('Comando incorrecto')

    def ComandoAgregar(self):
        return "A"

    def eligeComando(self,argument):
        switcher={
        1:self.ComandoAgregar()
        }
        return switcher.get(argument, lambda:"Opción inválida")

class AddProductWindow(QWidget):
    def __init__(self, elem):
        super().__init__()
        self.padre = elem
        self.setWindowTitle("Agregar producto")
        self.resize(480,480)
        self.layout = QVBoxLayout()
        self.labelSKU = QLabel()
        self.labelSKU.setText("Ingrese SKU:")
        self.inputSKU = QLineEdit()
        self.labelProducto = QLabel()
        self.labelProducto.setText("Ingrese nombre del producto:")
        self.inputProduct = QLineEdit()
        self.labelPrecio = QLabel()
        self.labelPrecio.setText("Ingese precio:")
        self.inputPrecio = QLineEdit()
        self.btnConfirm = QPushButton("Confirmar")
        self.btnConfirm.clicked.connect(self.confirmData)

        self.layout.addWidget(self.labelSKU)
        self.layout.addWidget(self.inputSKU)
        self.layout.addWidget(self.labelProducto)
        self.layout.addWidget(self.inputProduct)
        self.layout.addWidget(self.labelPrecio)
        self.layout.addWidget(self.inputPrecio)
        self.layout.addWidget(self.btnConfirm)
        self.setLayout(self.layout)

    def confirmData(self):
        price = self.inputPrecio.text()
        print("El precio es "+str(price))
        valor = [self.inputSKU.text(), self.inputProduct.text(), float(price)]
        self.padre.marco.setStyleSheet("QFrame{border: 1px solid black;}")
        self.padre.input.setStyleSheet("border: 1px solid black;")
        self.padre.datos.append(valor)
        self.padre.table.model().layoutChanged.emit()
        self.padre.calculateTotal()
        self.padre.inputCommands.hide()
        self.close()

    def displayInfo(self):
        self.show()

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
    # ...
    window = MainWindow()
    window.resize(600,600)
    window.show()
    app.exec_()
