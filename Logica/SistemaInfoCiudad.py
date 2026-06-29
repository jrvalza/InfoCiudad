from Logica.Coordenada import Coordenada
from Logica.PuntoInteres import PuntoInteres
from Persistencia.DataAccessLayer import DataAccessLayer


class SistemaInfoCiudad:
    def __init__(self):
        self.puntoInteres = None

        self.__identificador = None
        self.__dal = DataAccessLayer()

    @property
    def puntoInteres(self):
        return self.__puntoInteres

    @puntoInteres.setter
    def puntoInteres(self, value):
        self.__puntoInteres = value

    def conectar_bd(self, nombre):
        self.__dal.db_connect(nombre)
        self.__identificador = self.__dal.getMaxIdentificador()

    def desconectar_bd(self):
        return self.__dal.db_close()

    def exists_connection(self):
        return self.__dal.exists_connection()

    def get_next_idenficador(self):
        self.__identificador += 1
        return self.__identificador

    def crear_punto_interes(self, descripcion: str, latitud: float, longitud: float, etiqueta: str, color: str):
        identificador = "POI" + str(self.get_next_idenficador()).zfill(5)
        # Se crea el punto de interes
        coordenada = Coordenada(latitud, longitud)
        self.puntoInteres = PuntoInteres(identificador, descripcion, etiqueta, color, coordenada=coordenada)

    def buscar_punto_interes_descripcion(self, descripcion: str):
        return self.__dal.buscar_punto_interes_descripcion(descripcion)

    #=================================================METEREOLOGIA=================================================
    def buscarElementosEnArea(self, latitud, longitud, latitud1, longitud1):
        return self.__dal.buscarPuntosInteresEnArea(latitud, longitud, latitud1, longitud1)




    #=================================================VALENBICI=================================================
    def buscarValenBiciEnArea(self, latitud, longitud, latitud1, longitud1):
        return self.__dal.buscarPuntosValenBiciEnArea(latitud, longitud, latitud1, longitud1)




    def guardar_punto_interes(self):
        return self.__dal.guardar_puntoInteres(self.puntoInteres)

    def modificar_punto_interes(self, puntoInteres):
        return self.__dal.modificar_puntoInteres(puntoInteres)

    def borrar_punto_interes(self, identificador):
        return self.__dal.borrar_puntoInteres(identificador)

    def exists_changes(self):
        return self.__dal.exists_changes()

    def save_changes(self):
        return self.__dal.save_changes()

    def discard_changes(self):
        return self.__dal.discard_changes()



