from Logica.PuntoInteres import PuntoInteres


class PuntoInformaciónTiempo(PuntoInteres):
    def __init__(self, identificador: str, descripcion: str, etiqueta: str, color: str, dir_aproximada = None, coordenada = None):
        super().__init__(identificador, descripcion, etiqueta, color, dir_aproximada, coordenada)
        self.temperatura = 0
        self.humedad = 0

    @property
    def temperatura(self):
        return self.__temperatura

    @temperatura.setter
    def temperatura(self, valor):
        self.__temperatura = valor

    @property
    def humedad(self):
        return self.__humedad

    @humedad.setter
    def humedad(self, valor):
        self.__humedad = valor