import sqlite3


class DataAccessObject():
    def __init__(self, connection: sqlite3.Connection, idClase: int):
        if connection == None:
            raise ValueError("Se necesita una conexion para poder trabajar con la BD")
        self.__cursor = connection.cursor()
        self.__idClase = idClase

    @property
    def cursor(self):
        return self.__cursor

    @property
    def idClase(self):
        return self.__idClase