import math

from Logica.Coordenada import Coordenada


class AreaSeleccionada():
    KM_GRADO_LAT = 1 / 111.319 # dato wikipedia
    KM_GRADO_LNG = 1 / 111.131

    def __init__(self, centro: Coordenada, distancia: float):
        self.__centro = centro
        self.__distancia = distancia / 1000

    def getSuperiorIzquierda(self):
        return Coordenada(self.__centro.latitud - self.__distancia * AreaSeleccionada.KM_GRADO_LAT,
                          self.__centro.longitud - self.__distancia * AreaSeleccionada.KM_GRADO_LNG);

    def getInferiorDerecha(self):
        return Coordenada(self.__centro.latitud + self.__distancia * AreaSeleccionada.KM_GRADO_LAT,
                          self.__centro.longitud + self.__distancia * AreaSeleccionada.KM_GRADO_LNG);

    def perteneceArea(self, coordenada):
        lat1 = self.__centro.latitud
        lon1 = self.__centro.longitud
        lat2 = coordenada.latitud
        lon2 = coordenada.longitud
        RADIO = 6378.137 #  Radio de la tierra en km

        # Distancia entre dos coordenadas geograficas en metros -> si D <= radio, pertenece al circulo
        d = RADIO * math.acos(math.cos(self.__radianes(lat1)) * math.cos(self.__radianes(lat2)) * math.cos(self.__radianes(lon2 - lon1)) +
                      math.sin(self.__radianes(lat1)) * math.sin(self.__radianes(lat2)))
        return (d <= self.__distancia)

    def __radianes(self, valor):
        return valor * math.pi / 180
