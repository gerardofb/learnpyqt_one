from PySide2.QtWidgets import (
    QPushButton, QVBoxLayout, QLineEdit, QLabel, QWidget
    )

class AddProductWindow(QWidget):    
    def __init__(self, elem):
        super().__init__()
        self.padre = elem
        self.setWindowTitle('Agregar producto')
        self.resize(480,480)
        self.layout = QVBoxLayout()
        self.labelSKU = QLabel()
        self.labelSKU.setText('Ingrese SKU:')
        self.inputSKU = QLineEdit()
        self.labelProducto = QLabel()
        self.labelProducto.setText('Ingrese nombre del producto:')
        self.inputProduct = QLineEdit()
        self.labelPrecio = QLabel()
        self.labelPrecio.setText('Ingese precio:')
        self.inputPrecio = QLineEdit()
        self.btnConfirm = QPushButton('Confirmar')
        self.btnConfirm.clicked.connect(self.confirm_data)
        self.layout.addWidget(self.labelSKU)
        self.layout.addWidget(self.inputSKU)
        self.layout.addWidget(self.labelProducto)
        self.layout.addWidget(self.inputProduct)
        self.layout.addWidget(self.labelPrecio)
        self.layout.addWidget(self.inputPrecio)
        self.layout.addWidget(self.btnConfirm)
        self.setLayout(self.layout)

    def confirm_data(self):
        price = self.inputPrecio.text()
        valor = [self.inputSKU.text(), self.inputProduct.text(), float(price)]
        self.padre.marco.setStyleSheet("QFrame{border: 1px solid black;}")
        self.padre.input.setStyleSheet("border: 1px solid black;")
        self.padre.datos.append(valor)
        self.padre.table.model().layoutChanged.emit()
        self.padre.calculate_total()
        self.padre.inputCommands.hide()
        self.close()

    def display_info(self):
        self.show()
