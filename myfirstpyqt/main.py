# This Python file uses the following encoding: utf-8
from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QAction, QHBoxLayout, QPushButton, QVBoxLayout, 
    QTableView, QFrame, QLineEdit, QWidget, QLabel
    )
from PySide2.QtCore import Signal, QAbstractTableModel
from PySide2.QtWebEngineWidgets import QWebEngineView

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
        self.ventanaHelp.displayHelp()

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

class HelpContentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ayuda de la aplicación de cobro de Clean Market")
        self.navegador = QWebEngineView()
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.navegador)
        self.setLayout(vbox)


    def displayHelp(self):
        self.showHelp()
        self.showMaximized()

    def showHelp(self):
        self.html='''<!doctype html>
        <html lang="es">
        <head>
        <meta charset="utf-8">
        <title>Ayuda de aplicación de Cobro de Clean Market</title>
        <style type="text/css">
        /* Dropdown Button */
        h2, h4{
          color: teal;
          font-family: Arial, sans-serif;
        }
        article{
          background:lightgray;
          padding:1.5em;
          border-radius:10px;
          margin-top:1em;
        }
        p {
          color:brown;
          font-family:Helvetica, sans-serif;
          font-size:14px;
        }
        .dropbtn {
          background-color: #4CAF50;
          color: white;
          padding: 16px;
          font-size: 16px;
          border: none;
        }

        /* The container <div> - needed to position the dropdown content */
        .dropdown {
          position: relative;
          display: inline-block;
        }

        /* Dropdown Content (Hidden by Default) */
        .dropdown-content {
          display: none;
          position: absolute;
          background-color: #f1f1f1;
          min-width: 160px;
          box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
          z-index: 1;
        }

        /* Links inside the dropdown */
        .dropdown-content a {
          color: black;
          padding: 12px 16px;
          text-decoration: none;
          display: block;
        }

        /* Change color of dropdown links on hover */
        .dropdown-content a:hover {background-color: #ddd;}

        /* Show the dropdown menu on hover */
        .dropdown:hover .dropdown-content {display: block;}

        /* Change the background color of the dropdown button when the dropdown content is shown */
        .dropdown:hover .dropbtn {background-color: #3e8e41;}
        </style>
        </head>
        <body>
        <section name="inicio">
          <main>
            <h2>
            Ayuda de la aplicación de cobro de Clean Market
            </h2>
          </main>
        </section>
        <nav style="width:100%">
          <div class="dropdown">
          <button class="dropbtn">Menús</button>
          <div class="dropdown-content">
            <a href="#help_menu">Menú ayuda</a>
            <a href="#file_menu">Menú archivo</a>
          </div>
        </div>
          <div class="dropdown">
          <button class="dropbtn">Comandos</button>
          <div class="dropdown-content">
            <a href="#">Agregar producto</a>
            <a href="#">Borrar último registro</a>
            <a href="#">Borrar registros por SKU</a>
          </div>
          </div>
            <div class="dropdown">
          <button class="dropbtn">Atajos de teclado</button>
          <div class="dropdown-content">
            <a href="#">Menú ayuda</a>
            <a href="#">Menú archivo</a>
            <a href="#">Comandos</a>
          </div>
          </div>
        </nav>
        <hr />
        <section class="content">
        <main>
          <h2>
          Menús de la aplicación
          </h2>
        </main>
          <article>
            <h4>
            <a name="help_menu">
            Menú ayuda
            </a>
            </h4>
            <p>
            En este menú encontrarás el <a href="#submenu_help_content">contenido de esta ayuda</a> y también información de la licencia del producto.
            </p>
            <p>
            Puedes acceder al menú con la combinación de teclas Ctrl+h. E individualmente a las opciones "Contenido de la ayuda" y "Acerca de" con las combinaciones de teclas Ctrl+Mayúsculas+c y Ctrl+Mayúsculas+a respectivamente. Si deseas más información consulta la <a href="#key_shortcuts">sección de atajos de teclado</a>.
            </p>
          </article>
           <article>
            <h4>
            <a name="submenu_help_content">
            Menú ayuda, contenido de la ayuda
            </a>
            </h4>
            <p>
            En este submenú encontrarás el conenido de esta ayuda. Accede directamente a él con la combinacion de teclas Ctrl+Mayúsculas+c.
            </p>
            <p>
            </p>
          </article>
           <article>
            <h4>
            <a name="file_menu">
            Menú archivo
            </a>
            </h4>
            <p>
            Desde este menú puedes realizar la <a href="#submenu_file_print">impresión de tus cobros</a>, así como <a href="#submenu_file_new">iniciar un nuevo cobro</a> e <a href="#submenu_file_login">iniciar sesión en la aplicación</a> o bien <a href="#submenu_file_command">levantar una nueva consola de comandos</a>.</p>
            <p>
        Puedes acceder al menú con la combinación de teclas Ctrl+f, consulta mayor información en la <a href="#key_shortcuts">sección de atajos de teclado</a>.
            </p>
          </article>
           <article>
            <h4>
            <a name="submenu_file_print">
            Menú archivo, imprimir ticket de cobro
            </a>
            </h4>
            <p>
            Desde este submenú puedes realizar la impresión de un ticket de cobro, accede rápidamente a él con la combinación de teclas Ctrl+Mayúsculas+p.</p>
          </article>
           <article>
            <h4>
            <a name="submenu_file_new">
            Menú archivo, realizar un nuevo cobro
            </a>
            </h4>
            <p>
            Desde este submenú puedes iniciar un nuevo cobro, siempre y cuando hayas finalizado el anterior cobro. Accede a él con la combinación de teclas Ctrl+Mayúsculas+n</p>
          </article>
          <article>
            <h4>
            <a name="submenu_file_login">
            Menú archivo, iniciar o cerrar sesión
            </a>
            </h4>
            <p>
            Desde este submenú puedes iniciar sesión en la aplicación con tus credenciales o bien cerrar una sesión existente. Accede a él con la combinación de teclas Ctrl+Mayúsculas+l.
        </p>
          </article>
            <article>
            <h4>
            <a name="submenu_file_command">
            Menú archivo, consola de comandos
            </a>
            </h4>
            <p>
        Este submenú permite levantar una nueva ventana de comandos, es posible también realizar esta acción con la combinación de teclas Ctrl+Mayúsculas+m</p>
          </article>
        </section>
        </body>
        </html>'''
        self.navegador.setHtml(self.html)


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

class TableModel(QAbstractTableModel):
    def __init__(self, data, headerData):
                super(TableModel, self).__init__()
                self._data = data
                self.headerdata = headerData

    def data(self, index, role):
        if role == Qt.DisplayRole:
                    # See below for the nested-list data structure.
                    # .row() indexes into the outer list,
                    # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
                # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
                # The following takes the first sub-list, and returns
                # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.headerdata[col]
            return None

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
