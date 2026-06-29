from Persistencia.DataAccessObject import DataAccessObject


class DaoValenBici(DataAccessObject):
    def __init__(self, connection, idClase):
        super().__init__(connection, idClase)


    def buscar_punto_interes_area(self, latitud0, longitud0, latitud1, longitud1):

        sql = "SELECT identificador, nombre, latitud, longitud " \
              "FROM TablaInfoCiudad WHERE latitud BETWEEN ? AND ? AND idClase = ?" \
              "AND identificador IN( SELECT identificador FROM TablaInfoCiudad " \
              "WHERE  longitud BETWEEN ? AND ? AND idClase = ?)"
        self.cursor.execute(sql, (latitud0, latitud1, self.idClase, longitud0, longitud1, self.idClase))

        lista = self.cursor.fetchall()

        #=========PRUEBA===========
        print('DAO: ',len(lista))
        # =========PRUEBA===========


        return lista



