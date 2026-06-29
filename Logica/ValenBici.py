from Logica.PuntoInteres import PuntoInteres


class PuntoInformaciónValenBici(PuntoInteres):
    def __init__(self, identificador: str, descripcion: str, etiqueta: str, color: str, dir_aproximada = None, coordenada = None):
        super().__init__(identificador, descripcion, etiqueta, color, dir_aproximada, coordenada)
        self.bicicletasDisponibles = 0
        self.plazasLibres = 0

    @property
    def bicicletasDisponibles(self):
        return self.__bicicletasDisponibles

    @bicicletasDisponibles.setter
    def bicicletasDisponibles(self, valor):
        self.__bicicletasDisponibles = valor

    @property
    def plazasLibres(self):
        return self.__plazasLibres

    @plazasLibres.setter
    def plazasLibres(self, valor):
        self.__plazasLibres = valor