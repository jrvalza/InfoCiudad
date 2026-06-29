from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QProgressBar, QVBoxLayout, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView

class VentanaNavegador(QDialog):
    # El diálogo recibe el html a mostrar en su constructor
    def __init__(self, html_mapa : str):
        super().__init__()
        self.resize(640, 320)
        self.setWindowTitle('Mostrando un mapa')
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)

        # Control para mostrar contenido html
        self.web_view = QWebEngineView()
        self.web_view.setHtml(html_mapa)
        self.web_view.loadProgress.connect(self.webLoading)

        # Barra de prograso por si la carga del html es costosa
        self.progress = QProgressBar()
        self.progress.setValue(0)

        # Botón cerrar para terminar
        self.cerrar = QPushButton("Cerrar")
        self.cerrar.clicked.connect(self.close)

        # Diseño horizontal para alinear la barra y el botón
        self.progress_bar = QHBoxLayout()
        self.progress_bar.addWidget(self.progress)
        self.progress_bar.addWidget(self.cerrar)

        # Diseño vertical para el contenido web y el diseño horizontal
        root = QVBoxLayout()
        root.addWidget(self.web_view)
        root.addLayout(self.progress_bar)

        self.setLayout(root)

    # Actualización de la barra de progreso
    def webLoading(self, event):
        self.progress.setValue(event)




