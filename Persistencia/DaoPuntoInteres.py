from Persistencia.DataAccessObject import DataAccessObject


class DaoPuntoInteres(DataAccessObject):
    def __init__(self, connection, idClase):
        super().__init__(connection, idClase)

    def __crear_infoCiudad(self, identificador, nombre, latitud, longitud, idClase):
        sql = "insert into TablaInfoCiudad (identificador, nombre, latitud, longitud, idClase) " \
              "values (?,?,?,?,?)"
        self.cursor.execute(sql, (identificador, nombre, latitud, longitud, idClase))

    def __modificar_infoCiudad(self, identificador, nombre, latitud, longitud):
        sql = "UPDATE TablaInfoCiudad SET nombre=?, latitud=?, longitud=? WHERE identificador=?"
        self.cursor.execute(sql, (nombre, latitud, longitud, identificador))

    def __borrar_infoCiudad(self, identificador):
        sql = "DELETE FROM TablaInfoCiudad WHERE identificador=?"
        self.cursor.execute(sql, (identificador,))

    def guardar_puntoInteres(self, identificador, nombre, latitud, longitud, etiqueta, color):
        self.__crear_infoCiudad(identificador, nombre, latitud, longitud, self.idClase)
        sql = "INSERT INTO TablaPuntoInteres (identificador, etiqueta, color) values (?,?,?)"
        self.cursor.execute(sql, (identificador, etiqueta, color))

    def getMaxIdentificador(self):
        sql = "SELECT MAX(identificador) FROM TablaPuntoInteres WHERE identificador LIKE 'POI%'"
        self.cursor.execute(sql)
        valor = self.cursor.fetchone()
        if all(valor):
            return valor
        else:
            return ("POI0",)

    def buscar_punto_interes_descripcion(self, descripcion: str):
        sql = "SELECT ti.identificador, ti.nombre, ti.latitud, ti.longitud, tpi.etiqueta, tpi.color " \
              "FROM TablaInfoCiudad ti, TablaPuntoInteres tpi WHERE ti.identificador = tpi.identificador AND " \
              f"ti.nombre LIKE '%{descripcion}%'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def modificar_puntoInteres(self, identificador, nombre, latitud, longitud, etiqueta, color):
        self.__modificar_infoCiudad(identificador, nombre, latitud, longitud)

        sql = "UPDATE TablaPuntoInteres SET etiqueta=?, color=? WHERE identificador=?"
        self.cursor.execute(sql, (etiqueta, color, identificador))

    def borrar_puntoInteres(self, identificador):
        sql = f"DELETE FROM TablaPuntoInteres WHERE identificador=?"
        self.cursor.execute(sql, (identificador, ))
        self.__borrar_infoCiudad(identificador)

    def buscar_punto_interes_area(self, latitud0, longitud0, latitud1, longitud1):
        sql = "SELECT ti.identificador, ti.nombre, ti.latitud, ti.longitud " \
              "FROM TablaInfoCiudad ti, TablaPuntoInteres tpi WHERE ti.identificador = tpi.identificador AND" \
              " latitud BETWEEN ? AND ? and longitud BETWEEN ? AND ?"
        self.cursor.execute(sql, (latitud0, latitud1, longitud0, longitud1))
        return self.cursor.fetchall()
