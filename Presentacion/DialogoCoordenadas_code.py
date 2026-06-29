
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox
import geopy.geocoders as geocoders

class VentanaCoordenadas(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("Presentacion/DialogoCoordenadas_gui.ui", self)
        self.__latitud = None
        self.__longitud = None

        self.buttonBox.button(QDialogButtonBox.Ok).setText("Copiar")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.buttonBox.accepted.connect(self.fn_actualizar)
        self.pushButton_obtener.clicked.connect(self.fn_obtener)

    def fn_actualizar(self):
        self.__latitud = self.lineEdit_latitud.text()
        self.__longitud = self.lineEdit_longitud.text()


    def get_latitud_longitud(self):
        return self.__latitud, self.__longitud

    def fn_obtener(self):
        try:
            if self.lineEdit_direccion.text() != "":
                direccion_aproximada = self.lineEdit_direccion.text()
                geolocalizador = geocoders.Nominatim(user_agent="Interfaz Visual PAV")
                localizacion = geolocalizador.geocode(direccion_aproximada)
                self.lineEdit_latitud.setText(str(localizacion.latitude))
                self.lineEdit_longitud.setText(str(localizacion.longitude))
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
                self.buttonBox.button(QDialogButtonBox.Ok).setFocus()
            else:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                QMessageBox.critical(self, "Error", "La dirección aproximada no puede ser vacía.", QMessageBox.Ok)
        except Exception as ex:
            reply = QMessageBox.critical(self, "Error",
                                         f"Los datos no son correctos, no se ha podido obtener las coordenadas debido a:\n {ex} \n ¿Desea modificarlos?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                self.reject()

