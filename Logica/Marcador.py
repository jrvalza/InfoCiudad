from Logica.Coordenada import Coordenada

colors = ['red', 'blue', 'gray', 'darkred', 'lightred', 'orange', 'beige', 'green', 'darkgreen', 'lightgreen',
    'darkblue', 'lightblue', 'purple', 'darkpurple', 'pink', 'cadetblue', 'lightgray', 'black']

class Marcador():
    def __init__(self, coordenada: Coordenada, etiqueta: str, color: str):
        self.coordenada = coordenada
        self.etiqueta = etiqueta
        self.color = color

    def __str__(self):
        return f"Marcador con {self.coordenada}, etiqueta: {self.etiqueta} y color: {self.color}"

    def __repr__(self):
        return f"Marcador[{self.coordenada}, {self.etiqueta}, {self.color}]"

    def __eq__(self, other):
        return self.coordenada == other.coordenada and self.etiqueta == other.etiqueta

    @property
    def coordenada(self):
        return self.__coordenada

    @coordenada.setter
    def coordenada(self, value: Coordenada):
        self.__coordenada = value

    @property
    def etiqueta(self):
        return self.__etiqueta

    @etiqueta.setter
    def etiqueta(self, value):
        self.__etiqueta = value

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        if value not in colors:
            raise ValueError("El color introducido no es un color válido, recuerda que debe ser un color en inglés.")
        self.__color = value