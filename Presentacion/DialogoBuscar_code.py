from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QTableWidgetItem

from Logica.SistemaInfoCiudad import SistemaInfoCiudad
from Presentacion.DialogoPuntoInteres_code import VentanaPuntoInteres


class VentanaBuscar(QDialog):
    def __init__(self, sistema: SistemaInfoCiudad):
        super().__init__()
        uic.loadUi("Presentacion/DialogoBuscar_gui.ui", self)
        self.__sistema = sistema
        self.__identificador = None
        self.__diccionario_puntos = {}

        self.buttonBox.button(QDialogButtonBox.Ok).setText("Seleccionar")
        self.buttonBox.button(QDialogButtonBox.Save).setText("Modificar")
        self.buttonBox.button(QDialogButtonBox.Close).setText("Borrar")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Cerrar")
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.fn_seleccionar)
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.fn_modificar)
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.fn_borrar)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.fn_cerrar)
        self.pushButton_buscar.clicked.connect(self.fn_buscar)
        self.tableWidget_puntos.itemClicked.connect(self.fn_fila_seleccion)
        self.tableWidget_puntos.itemSelectionChanged.connect(self.fn_fila_seleccion)

    def fn_fila_seleccion(self):
        selected = self.tableWidget_puntos.currentIndex()
        if not selected.isValid() or len(self.tableWidget_puntos.selectedItems()) < 1:
            return
        self.__identificador = self.tableWidget_puntos.item(selected.row(), 0).text()

    def fn_buscar(self):
        try:
            if self.lineEdit_descripcion.text() == "":
                QMessageBox.critical(self, "Error",
                                     "Se debe indicar la descripción para poder buscar.", QMessageBox.Ok)
            else:
                self.__identificador = None
                self.__diccionario_puntos = self.__sistema.buscar_punto_interes_descripcion(self.lineEdit_descripcion.text())
                # Vamos a añadir el resultado
                self.mostrar_resultado()
        except Exception as ex:
            QMessageBox.critical(self, "Error",
                             f"No se ha podido conectar la base de datos debido a:\n {ex} \n")

    def mostrar_resultado(self):
        self.tableWidget_puntos.clearContents()
        self.tableWidget_puntos.setRowCount(0)
        for clave in self.__diccionario_puntos:
            punto = self.__diccionario_puntos[clave]
            index = self.tableWidget_puntos.rowCount()
            self.tableWidget_puntos.setRowCount(index + 1)
            self.tableWidget_puntos.setItem(index, 0, QTableWidgetItem(punto.identificador))  # Columna identificador
            self.tableWidget_puntos.setItem(index, 1, QTableWidgetItem(punto.descripcion))  # Columna descripción
            self.tableWidget_puntos.setItem(index, 2,
                                            QTableWidgetItem(str(punto.marcador.coordenada.latitud)))  # Columna latitud
            self.tableWidget_puntos.setItem(index, 3, QTableWidgetItem(
                str(punto.marcador.coordenada.longitud)))  # Columna longitud
            self.tableWidget_puntos.setItem(index, 4, QTableWidgetItem(punto.marcador.etiqueta))  # Columna etiqueta
            self.tableWidget_puntos.setItem(index, 5, QTableWidgetItem(punto.marcador.color))  # Columna color

    def fn_seleccionar(self):
        if not self.__identificador == None:
            self.__sistema.puntoInteres = self.__diccionario_puntos[self.__identificador]
            self.accept()

    def fn_cerrar(self):
        self.reject()

    def fn_modificar(self):
        if not self.__identificador == None:
            try:
                ventanaPuntoInteres = VentanaPuntoInteres(self.__sistema, punto=self.__diccionario_puntos[self.__identificador])

                respuesta = ventanaPuntoInteres.exec_()
                if respuesta == QDialog.Accepted:
                    self.mostrar_resultado()
            except Exception as ex:
                print(ex)


    def fn_borrar(self):
        if not self.__identificador == None:
            reply = QMessageBox.question(self, "Borrar punto interes",
                                         "Se va a eliminar el punto de interes.\n ¿Esta seguro?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if self.__sistema.borrar_punto_interes(self.__identificador):
                    mensaje = "El Punto de Interés se ha borrado correctamente."
                    self.fn_buscar()
                else:
                    mensaje = "El Punto de Interés no se ha borrado."
            else:
                mensaje = "El Punto de Interés no se ha borrado."

            QMessageBox.information(self, "Guardar Punto de Interes", mensaje)