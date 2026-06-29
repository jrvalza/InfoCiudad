from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox

from Logica.Marcador import colors
from Logica.SistemaInfoCiudad import SistemaInfoCiudad
from Presentacion.DialogoCoordenadas_code import VentanaCoordenadas


class VentanaPuntoInteres(QDialog):
    def __init__(self, sistema: SistemaInfoCiudad, punto = None, grabar = False):
        super().__init__()
        uic.loadUi("Presentacion/DialogoPuntoInteres_gui.ui", self)
        self.__sistema = sistema
        self.__grabar = grabar
        self.__punto = punto

        if self.__grabar:
            self.buttonBox.button(QDialogButtonBox.Ok).setText("Grabar")
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setText("Crear")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancelar")

        self.buttonBox.accepted.connect(self.fn_crear)

        self.comboBox_color.addItems(colors)
        self.comboBox_color.setCurrentIndex(0)

        self.pushButton_introducir.clicked.connect(self.fn_obtener_coordenadas)

        # rellenamos los controles
        if not self.__punto == None:
            self.buttonBox.button(QDialogButtonBox.Ok).setText("Modificar")
            self.lineEdit_descripcion.setText(self.__punto.descripcion)
            self.lineEdit_latitud.setText(str(self.__punto.marcador.coordenada.latitud))
            self.lineEdit_longitud.setText(str(self.__punto.marcador.coordenada.longitud))
            self.lineEdit_etiqueta.setText(self.__punto.marcador.etiqueta)
            indice = colors.index(self.__punto.marcador.color)
            self.comboBox_color.setCurrentIndex(indice)

    def fn_crear(self):
        if self.lineEdit_descripcion.text() == "" or self.lineEdit_latitud.text() == "" or \
                self.lineEdit_longitud.text() == "" or self.lineEdit_etiqueta.text() == "":
            QMessageBox.critical(self, "Error",
                                 "Se deben completar todos los campos.", QMessageBox.Ok)
        else:
            try:
                # Se crea el punto de interes
                if self.__punto == None:
                    self.__sistema.crear_punto_interes(self.lineEdit_descripcion.text(), float(self.lineEdit_latitud.text()),
                                                   float(self.lineEdit_longitud.text()),self.lineEdit_etiqueta.text(), self.comboBox_color.currentText())
                    if self.__grabar:
                        self.__sistema.guardar_punto_interes()
                else:
                    self.__punto.descripcion = self.lineEdit_descripcion.text()
                    self.__punto.marcador.coordenada.latitud = float(self.lineEdit_latitud.text())
                    self.__punto.marcador.coordenada.longitud = float(self.lineEdit_longitud.text())
                    self.__punto.marcador.etiqueta = self.lineEdit_etiqueta.text()
                    self.__punto.marcador.color = self.comboBox_color.currentText()
                    self.__sistema.modificar_punto_interes(self.__punto)
                self.accept()
            except Exception as ex:
                reply = QMessageBox.critical(self, "Error",
                                             f"Los datos no son correctos, no se ha podido crear el punto de interés debido a:\n {ex} \n ¿Desea modificarlos?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    self.reject()

    def fn_obtener_coordenadas(self):
            ventanaCoordenadas = VentanaCoordenadas()

            respuesta = ventanaCoordenadas.exec_()

            if respuesta == QDialog.Accepted:
                latitud, longitud = ventanaCoordenadas.get_latitud_longitud()
                self.lineEdit_latitud.setText(latitud)
                self.lineEdit_longitud.setText(longitud)



