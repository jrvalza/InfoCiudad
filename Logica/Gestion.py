import folium

from Logica.AreaSeleccionada import AreaSeleccionada
from Logica.Marcador import colors
from Logica.SistemaInfoCiudad import SistemaInfoCiudad
from Persistencia.ApiServicioWeb import ApiServicioWeb


class Gestion():

    def __init__(self, sistema: SistemaInfoCiudad, dato: int):
        self.__sistema = sistema
        self.__dato = dato
        self.__area = AreaSeleccionada(sistema.puntoInteres.marcador.coordenada, dato)
        self.__apiWeb = ApiServicioWeb()
        self.__infoSeleccionada = []
        # Crearmos un mapa y añadimos el punto de interés como un marcador más
        self.__mapa = self.__crear_mapa()


    def __crear_mapa(self):
        return folium.Map(
            location=[self.__sistema.puntoInteres.marcador.coordenada.latitud,
                      self.__sistema.puntoInteres.marcador.coordenada.longitud],
            tiles='openstreetmap',
            zoom_start=14)

    def __add_marcador(self, puntoInteres):
        folium.Marker(
            location=[puntoInteres.marcador.coordenada.latitud,
                      puntoInteres.marcador.coordenada.longitud],
            popup=puntoInteres.marcador.etiqueta,
            icon=folium.Icon(color=puntoInteres.marcador.color)
        ).add_to(self.__mapa)

    def obtener_html(self):
        return self.__mapa.get_root().render()

    #=================================================METEREOLOGIA=================================================
    def consultaElementoArea(self):
        if self.__sistema.puntoInteres == None:
            raise ValueError("Se debe crear el punto de interés antes de consultar los elementos cercanos.")
        if self.__area == None:
            raise ValueError("Se debe definir el área seleccionada antes de consultar los elementos cercanos.")

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Añadimos el punto de interés como un marcador más
        self.__add_marcador(self.__sistema.puntoInteres)

        # Buscamos los elemementos que están dentro del cuadrado del área seleccionada
        elementosEnArea = self.__sistema.buscarElementosEnArea(self.__area.getSuperiorIzquierda().latitud,
                                                               self.__area.getSuperiorIzquierda().longitud,
                                                               self.__area.getInferiorDerecha().latitud,
                                                               self.__area.getInferiorDerecha().longitud)

        indice_letra = 0
        indice_color = 0
        for elemento in elementosEnArea:
            # Si algún elemento seleccionado es el mismo que el centro, no se hace nada con ese elemento
            if elemento.marcador.coordenada == self.__sistema.puntoInteres.marcador.coordenada:
                continue
            #  Comprobamos que realmente pertenecen al área seleccionada(circulo)
            if self.__area.perteneceArea(elemento.marcador.coordenada):
                #  Buscamos la información que falta en el Servicio Web
                temperatura, humedad = self.__apiWeb.get_info_meteorologica(elemento.marcador.coordenada.latitud,
                                                                            elemento.marcador.coordenada.longitud)
                if temperatura is None and humedad is None:
                    continue

                # Añadimos la información que falta etiqueta, color e información del servicio web meteorológico (temperatura y humedad)
                elemento.marcador.etiqueta = letras[indice_letra % 27]
                indice_letra += 1
                color = colors[indice_color % 18]
                indice_color += 1
                if color == self.__sistema.puntoInteres.color:
                    color = colors[indice_color % 18]
                    indice_color += 1
                elemento.color = color

                # Añandimos la información particular del elemento
                elemento.temperatura = temperatura
                elemento.humedad = humedad

                # Añadimos a la lista
                self.__infoSeleccionada.append(elemento)

                # Añadir el marcador al mapa
                self.__add_marcador(elemento)
        return self.__infoSeleccionada


    # =================================================VALENBICI=================================================
    def consultaValenBiciArea(self):
        if self.__sistema.puntoInteres == None:
            raise ValueError("Se debe crear el punto de interés antes de consultar los elementos cercanos.")

        if self.__area == None:
            raise ValueError("Se debe definir el área seleccionada antes de consultar los elementos cercanos.")

        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Añadimos el punto de interés como un marcador más
        self.__add_marcador(self.__sistema.puntoInteres)

        # Buscamos los elemementos que están dentro del cuadrado del área seleccionada
        elementosEnArea = self.__sistema.buscarValenBiciEnArea(self.__area.getSuperiorIzquierda().latitud,
                                                               self.__area.getSuperiorIzquierda().longitud,
                                                               self.__area.getInferiorDerecha().latitud,
                                                               self.__area.getInferiorDerecha().longitud)
        #=========PRUEBA===========
        print('Gestión:', len(elementosEnArea))
        # =========PRUEBA===========

        indice_letra = 0
        #indice_color = 0
        indice_numero = 0 #Para utilizar la letra junto a un valor numerico, ejemplo: A_1, A_2
        for elemento in elementosEnArea:

            # Si algún elemento seleccionado es el mismo que el centro, no se hace nada con ese elemento
            if elemento.marcador.coordenada == self.__sistema.puntoInteres.marcador.coordenada:
                continue

            #  Comprobamos que realmente pertenecen al área seleccionada(circulo)
            if self.__area.perteneceArea(elemento.marcador.coordenada):


                #  Buscamos la información que falta en el Servicio Web
                ValenBici_libres, ValenBici_disponibles = self.__apiWeb.get_valenbici_info(elemento.marcador.coordenada.latitud,
                                                                                           elemento.marcador.coordenada.longitud)

                if ValenBici_disponibles is None and ValenBici_libres is None:
                    continue

                # Añadimos la información que falta etiqueta, color e información del servicio web ValenBici (bicicletas disponibles y plazas libres)
                elemento.marcador.etiqueta = letras[indice_letra % 27] + f'{indice_numero}'

                indice_letra += 1
                indice_numero +=1

                #Para resetear valores de variables auxiliares
                if indice_letra >= 26:
                    indice_letra = 0

                elemento.color = 'blue'

                # Añandimos la información particular del elemento
                elemento.bicicletasDisponibles = ValenBici_disponibles
                elemento.plazasLibres = ValenBici_libres

                # Añadimos a la lista
                self.__infoSeleccionada.append(elemento)

                # Añadir el marcador al mapa
                self.__add_marcador(elemento)

        #=========PRUEBA===========
        print(f'Total ValenBici en área: {len(self.__infoSeleccionada)}')
        # =========PRUEBA===========

        return self.__infoSeleccionada

