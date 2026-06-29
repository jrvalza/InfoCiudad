from geopy import Nominatim

import folium

from Logica.Coordenada import Coordenada
from Logica.Marcador import Marcador


class PuntoInteres():
    def __init__(self, identificador: str, descripcion: str, etiqueta: str, color: str, dir_aproximada = None, coordenada = None):
        if (dir_aproximada == None and coordenada == None) or (dir_aproximada != None and coordenada != None):
            raise TypeError("Tipo no correcto")
        self.__identificador = identificador
        self.descripcion = descripcion
        geolocalizador = Nominatim(user_agent="Caso 1 PAV")
        if dir_aproximada != None:
            localizacion = geolocalizador.geocode(dir_aproximada)
            coordenada = Coordenada(localizacion.latitude, localizacion.longitude)
        self.__marcador = Marcador(coordenada, etiqueta, color)
        localizacion = geolocalizador.reverse(repr(coordenada))
        self.__dirección_exacta = localizacion.address

    @property
    def identificador(self):
        return self.__identificador

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, value):
        self.__descripcion = value

    @property
    def marcador(self) -> Marcador:
        return self.__marcador

    @property
    def dirección_exacta(self):
        return self.__dirección_exacta

    @property
    def etiqueta(self):
        return self.marcador.etiqueta

    @etiqueta.setter
    def etiqueta(self, value):
        self.marcador.etiqueta = value

    @property
    def color(self):
        return self.marcador.color

    @color.setter
    def color(self, value):
        self.marcador.color = value

    def obtener_mapa(self):
        m = folium.Map(
            location=[self.marcador.coordenada.latitud, self.marcador.coordenada.longitud],
            tiles='openstreetmap',
            zoom_start=14)
        folium.Marker(
            location=[self.marcador.coordenada.latitud, self.marcador.coordenada.longitud],
            popup=self.marcador.etiqueta,
            icon=folium.Icon(color=self.marcador.color)
        ).add_to(m)
        return m

    def obtener_html(self):
        return self.obtener_mapa().get_root().render()


