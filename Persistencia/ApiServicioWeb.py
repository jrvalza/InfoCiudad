import requests

class ApiServicioWeb():

    def __init__(self):
        self.__apiweathermap = '75810bd0b2b5a73aa675b29707a800e7'
        self.__valenbisi_url = f"https://geoportal.valencia.es/server/rest/services/OPENDATA/Trafico/MapServer/228/query"


    # =================================================METEREOLOGIA=================================================
    def get_info_meteorologica(self,latitud, longitud):
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&lang=es&appid={self.__apiweathermap}&units=metric')
        respuesta = r.json()
        temperatura = respuesta["main"]["temp"]
        humedad = respuesta["main"]["humidity"]
        return temperatura, humedad


    # =================================================VALENBICI=================================================

    def get_valenbici_info(self, latitud, longitud):
        params = {
            "where": "1=1",
            "outFields": "*",
            "geometry": f"{longitud},{latitud}",   # ArcGIS espera lon,lat
            "geometryType": "esriGeometryPoint",
            "inSR": "4326",
            "spatialRel": "esriSpatialRelIntersects",
            "distance": 1,
            "units": "esriSRUnit_Meter",
            "f": "geojson",
        }

        r = requests.get(self.__valenbisi_url, params=params)

        if r.status_code != 200:
            print("Error API Valenbisi:", r.status_code, r.text)
            return None, None
            
        resultado = r.json()
        feature = resultado.get("features",[])

        if not feature:
            return None, None
        
        properties = feature[0]["properties"]

        free = properties.get("free")
        available = properties.get("available")

        return int(free), int(available)
