
import sys

from PyQt5.QtWidgets import QApplication

from Logica.SslConfig import SslContext
from Logica.SistemaInfoCiudad import SistemaInfoCiudad
from Presentacion.Principal_code import VentanaPrincipal


if __name__ == '__main__':
    SslContext()
    sistema = SistemaInfoCiudad()
    app = QApplication(sys.argv)
    GUI = VentanaPrincipal(sistema)
    GUI.show()
    sys.exit(app.exec_())


