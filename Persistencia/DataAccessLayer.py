import sqlite3

from Logica.Coordenada import Coordenada
from Logica.PuntoInformacónTiempo import PuntoInformaciónTiempo
from Logica.PuntoInteres import PuntoInteres
from Persistencia.DaoPuntoInteres import DaoPuntoInteres


from Persistencia.DaoValenBici import DaoValenBici
from Logica.ValenBici import PuntoInformaciónValenBici


class DataAccessLayer():
    def __init__(self):
        self.__db_connection: sqlite3.Connection = None
        self.__daoPuntoInteres = None
        self.__daoParking = None
        self.__daoValenbici = None
        self.__daoMonumento = None
        self.__daoRuta = None
        self.__daoParadaEMT = None
        self.__daoEstacionMetro = None
        self.__cursor = None

    def __buscar_clase(self, descripcion):
        sql = f"select * from TablaClase where descripcion = '{descripcion}'"
        self.__cursor.execute(sql)
        return self.__cursor.fetchone()[0]


    def __crear_DaoPuntoInteres(self):
        clave = self.__buscar_clase("Punto interés")
        self.__daoPuntoInteres = DaoPuntoInteres(self.__db_connection, clave)


    # =================================================DAO VALENBICI=================================================
    def __crear_DaoValenBici(self):
        clave = self.__buscar_clase("Estación ValenBici")
        self.__daoValenbici = DaoValenBici(self.__db_connection, clave)



    def db_connect(self, nameDb):
        try:
            self.__db_connection = sqlite3.connect(nameDb)
            self.__cursor = self.__db_connection.cursor()
            return True
        except Exception:
            return False



    def db_close(self):
        if not self.__db_connection == None:
            self.__db_connection.close()
            self.__db_connection = None

    def exists_connection(self):
        if self.__db_connection == None:
            return False
        else:
            return True

    def exists_changes(self):
        if self.__db_connection == None:
            return False
        else:
            return self.__db_connection.in_transaction

    def save_changes(self):
        if not self.__db_connection == None:
            self.__db_connection.commit()

    def discard_changes(self):
        if not self.__db_connection == None:
            self.__db_connection.rollback()

    def guardar_puntoInteres(self, punto: PuntoInteres):
        try:
            if self.__daoPuntoInteres == None:
                self.__crear_DaoPuntoInteres()

            self.__daoPuntoInteres.guardar_puntoInteres(punto.identificador, punto.descripcion,
                                                        punto.marcador.coordenada.latitud,
                                                        punto.marcador.coordenada.longitud, punto.etiqueta, punto.color)
            return True
        except Exception:
            return False

    def getMaxIdentificador(self):
        if self.__daoPuntoInteres == None:
            self.__crear_DaoPuntoInteres()

        str_ident = self.__daoPuntoInteres.getMaxIdentificador()
        str_ident = str_ident[0].lstrip("POI")
        return int(str_ident)

    def buscar_punto_interes_descripcion(self, descripcion: str):
        consulta = self.__daoPuntoInteres.buscar_punto_interes_descripcion(descripcion)
        resultado = {}
        for identificador, descripcion, latitud, longitud, etiqueta, color in consulta:
            resultado[identificador] = PuntoInteres(identificador, descripcion, etiqueta, color,
                                                    coordenada=Coordenada(latitud, longitud))
        return resultado

    def modificar_puntoInteres(self, punto):
        try:
            if self.__daoPuntoInteres == None:
                self.__crear_DaoPuntoInteres()

            self.__daoPuntoInteres.modificar_puntoInteres(punto.identificador, punto.descripcion,
                                                        punto.marcador.coordenada.latitud,
                                                        punto.marcador.coordenada.longitud, punto.etiqueta, punto.color)
            return True
        except Exception:
            return False

    def borrar_puntoInteres(self, identificador):
        try:
            if self.__daoPuntoInteres == None:
                self.__crear_DaoPuntoInteres()

            self.__daoPuntoInteres.borrar_puntoInteres(identificador)
            return True
        except Exception:
            return False

    # =================================================METEREOLOGIA=================================================
    def buscarPuntosInteresEnArea(self, latitud0, longitud0, latitud1, longitud1):
        consulta = self.__daoPuntoInteres.buscar_punto_interes_area(latitud0, longitud0, latitud1, longitud1)
        resultado = []
        for identificador, descripcion, latitud, longitud in consulta:
            resultado.append(PuntoInformaciónTiempo(identificador, descripcion, "una_etiqueta", "red", coordenada=Coordenada(latitud, longitud)))
        return resultado # Se devuelve el resultado como una lista





    # =================================================VALENBICI=================================================
    def buscarPuntosValenBiciEnArea(self, latitud0, longitud0, latitud1, longitud1):

        self.__crear_DaoValenBici()
        consulta = self.__daoValenbici.buscar_punto_interes_area(latitud0, longitud0, latitud1, longitud1)
        resultado = []

        for identificador, descripcion, latitud, longitud in consulta:
            resultado.append(PuntoInformaciónValenBici(identificador, descripcion, "una_etiqueta", "red", coordenada=Coordenada(latitud, longitud)))

        #=========PRUEBA===========
        print('DAL:', len(resultado))
        # =========PRUEBA===========

        return resultado # Se devuelve el resultado como una lista