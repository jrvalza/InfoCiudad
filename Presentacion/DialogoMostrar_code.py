from PyQt5 import uic, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from Logica.Gestion import Gestion

class VentanaMostrar(QDialog):
    def __init__(self, gestion: Gestion):
        super().__init__()
        uic.loadUi("Presentacion/DialogoMostrar_gui.ui", self)
        self.__gestion = gestion

        self.widget = QWebEngineView()
        self.widget.setMinimumSize(QtCore.QSize(640, 0))
        self.widget.setObjectName("widget")
        self.horizontalLayout.insertWidget(0, self.widget)

        self.obtener_resultado()
        self.widget.setHtml(self.__gestion.obtener_html())

    def obtener_resultado(self):
        infoElementos = self.__gestion.consultaElementoArea()
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        for puntoInformacionMeteo in infoElementos:
            index = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(index + 1)
            self.tableWidget.setItem(index, 0, QTableWidgetItem(puntoInformacionMeteo.descripcion))  # Columna nombre
            self.tableWidget.setItem(index, 1, QTableWidgetItem(puntoInformacionMeteo.marcador.etiqueta))  # Columna letra
            self.tableWidget.setItem(index, 2, QTableWidgetItem(puntoInformacionMeteo.marcador.color))  # Columna color
            self.tableWidget.setItem(index, 3, QTableWidgetItem(str(puntoInformacionMeteo.temperatura)+'º'))  # Columna temperatura
            self.tableWidget.setItem(index, 4, QTableWidgetItem(str(puntoInformacionMeteo.humedad)+'%'))  # Columna humedad