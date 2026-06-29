class Coordenada():
    def __init__(self, latitud: float, longitud: float):
        self.latitud = latitud
        self.longitud = longitud

    def __str__(self):
        return f"Coordenada de latitud: {self.latitud} y longitud: {self.longitud}"

    def __repr__(self):
        return f"{self.latitud}, {self.longitud}"

    def __eq__(self, other):
        if other == None:
            return False
        return self.latitud == other.latitud and self.longitud == other.longitud

    @property
    def latitud(self):
        return self.__latitud

    @latitud.setter
    def latitud(self, value):
        self.__latitud = value

    @property
    def longitud(self):
        return self.__longitud

    @longitud.setter
    def longitud(self, value):
        self.__longitud = value

