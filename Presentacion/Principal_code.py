from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox, QDialog

from Logica.Gestion import Gestion
from Logica.SistemaInfoCiudad import SistemaInfoCiudad
from Presentacion.DialogoBuscar_code import VentanaBuscar
from Presentacion.DialogoMostrar_code import VentanaMostrar
from Presentacion.DialogoMostrarValenBici_code import VentanaMostrarValenBici
from Presentacion.Navegador import VentanaNavegador
from Presentacion.DialogoPuntoInteres_code import VentanaPuntoInteres


class VentanaPrincipal(QMainWindow):
    def __init__(self, sistema: SistemaInfoCiudad):
        super().__init__()
        uic.loadUi("Presentacion/Principal_gui.ui", self)
        self.__sistema = sistema
        self.__nuevo = False

        self.actionSalir.triggered.connect(self.close)
        self.actionCrear.triggered.connect(self.fn_crear_punto_interes)
        self.actionConectar_base_de_datos.triggered.connect(self.fn_conectar)
        self.actionDesconectar_base_de_datos.triggered.connect(self.fn_desconectar)
        self.actionGuardar.triggered.connect(self.fn_guardar)
        self.actionBuscar.triggered.connect(self.fn_buscar)
        self.actionVer_mapa.triggered.connect(self.fn_ver_mapa)
        self.actionGuardar_los_cambios.triggered.connect(self.fn_guardarCambios)
        self.actionRechazar_los_cambios.triggered.connect(self.fn_rechazarCambios)

        self.actionMostrar_informaci_n_Meteorol_gica.triggered.connect(self.fn_mostrar_tiempo)
        self.actionMostrar_estaciones_ValenBici.triggered.connect(self.fn_mostrar_valenbici)
        self.actionMostrar_Parkings.triggered.connect(self.fn_mostrar_parking)
        self.actionMostrar_monumentos_en_area.triggered.connect(self.fn_mostrar_monumentos)
        self.actionMostrar_monumentos_en_ruta.triggered.connect(self.fn_mostrar_monumentos_ruta)
        self.actionMostrar_paradas_EMT.triggered.connect(self.fn_mostrar_paradas_emt)
        self.actionMostrar_estaciones_metro.triggered.connect(self.fn_mostrar_estaciones_metro)

        self.cambiar_habilitar_menus(False)


    def cambiar_habilitar_menus(self, valor):
        self.cambiar_habilitar_menus_punto(valor)
        if not valor:
            self.cambiar_habilitar_menus_consulta(valor)
        self.actionGuardar_los_cambios.setEnabled(valor)
        self.actionRechazar_los_cambios.setEnabled(valor)
        self.actionDesconectar_base_de_datos.setEnabled(valor)

    def cambiar_habilitar_menus_punto(self, valor):
        self.menuPunto_Inter_s.setEnabled(valor)

    def cambiar_habilitar_menus_consulta(self, valor):
        self.menuConsultar.setEnabled(valor)

    def closeEvent(self, event):
        if self.fn_desconectar():
            event.accept()
        else:
            event.ignore()

    def fn_crear_punto_interes(self):
        try:
            ventanaPuntoInteres = VentanaPuntoInteres(self.__sistema)

            respuesta = ventanaPuntoInteres.exec_()

            if respuesta == QDialog.Accepted:
                html_mapa = self.__sistema.puntoInteres.obtener_html()
                navegador = VentanaNavegador(html_mapa)
                navegador.exec()
                self.cambiar_habilitar_menus_consulta(True)
                self.__nuevo = True

        except Exception as ex:
            reply = QMessageBox.critical(self, "Error",
                                         f"No se ha podido crear el punto de interés debido a:\n {ex} \n ¿Desea continuar?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                self.close()

    def fn_conectar(self):
        try:
            self.__sistema.conectar_bd("Database\datosValencia.db")
            # Activar menus
            self.cambiar_habilitar_menus(True)
        except Exception as ex:
            QMessageBox.critical(self, "Error",
                                 f"No se ha podido conectar la base de datos debido a:\n {ex} \n")

    def fn_desconectar(self):
        desconectar = True
        if self.__sistema.exists_changes():
            reply = QMessageBox.question(self, "Existen cambios",
                                         "Existen cambios pendientes.\n ¿Desea guardar los cambios?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.__sistema.save_changes()
            elif reply == QMessageBox.No:
                self.__sistema.discard_changes()

            if reply == QMessageBox.Cancel:
                desconectar = False

        if desconectar:
            self.__sistema.desconectar_bd()
            # Desactivar menus
            self.cambiar_habilitar_menus(False)
            return True
        else:
            return False

    def fn_guardar(self):
        items = ["Un punto de interés nuevo"]
        if self.__nuevo:
            items.append("Un punto de interés creado previamente")
        value, ok = QInputDialog.getItem(self, "Seleccionar opción", "Qué desea guardar:", items, 0, False)
        if ok:
            if value == "Un punto de interés nuevo":
                ventanaPuntoInteres = VentanaPuntoInteres(self.__sistema, grabar=True)
                respuesta = ventanaPuntoInteres.exec_()
                if respuesta == QDialog.Accepted:
                    self.__nuevo = False
                    self.cambiar_habilitar_menus_consulta(True)
            else:
                if self.__sistema.guardar_punto_interes():
                    mensaje = "El Punto de Interés se ha guardado correctamente."
                    self.__nuevo = False
                else:
                    mensaje = "El Punto de Interés no se ha guardado."
                QMessageBox.information(self, "Guardar Punto de Interes", mensaje)

    def fn_buscar(self):
        ventanaBuscar = VentanaBuscar(self.__sistema)
        respuesta = ventanaBuscar.exec_()
        if respuesta == QDialog.Accepted:
            self.cambiar_habilitar_menus_consulta(True)

    def fn_ver_mapa(self):
        if self.__sistema.puntoInteres == None:
            QMessageBox.critical(self, "Error",
                                     "No hay punto de interes, debe crearlo o seleccionar alguno almacenado.", QMessageBox.Ok)
        else:
            html_mapa = self.__sistema.puntoInteres.obtener_html()
            navegador = VentanaNavegador(html_mapa)
            navegador.exec()

    def fn_guardarCambios(self):
        self.__sistema.save_changes()

    def fn_rechazarCambios(self):
        if self.__sistema.exists_changes():
            reply = QMessageBox.question(self, "Existen cambios",
                                         "Los cambios pendientes se perderán.\n ¿Desea continuar?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.__sistema.discard_changes()


    def fn_mostrar_tiempo(self):
        # Se pide el radio
        value, ok = QInputDialog.getInt(self, "Información requerida", "Introduce el radio:")
        if ok:
            gestion = Gestion(self.__sistema, value)
            ventanaMostrar = VentanaMostrar(gestion)
            respuesta = ventanaMostrar.exec_()

    def fn_mostrar_valenbici(self):
        # Se pide el radio
        value, ok = QInputDialog.getInt(self, "Información requerida", "Introduce el radio:")
        if ok:
            gestion = Gestion(self.__sistema, value)
            ventanaMostrar = VentanaMostrarValenBici(gestion)
            respuesta = ventanaMostrar.exec_()

    def fn_mostrar_parking(self):
        pass

    def fn_mostrar_monumentos(self):
        pass

    def fn_mostrar_monumentos_ruta(self):
        pass

    def fn_mostrar_paradas_emt(self):
        pass

    def fn_mostrar_estaciones_metro(self):
        pass