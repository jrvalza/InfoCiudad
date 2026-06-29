import ssl
import certifi
import geopy.geocoders as geocoders

class SslContext:
    def __init__(self, ctx: ssl.SSLContext = None):
        if ctx is None:
            ctx = ssl.create_default_context(cafile=certifi.where())
        self.__ctx = ctx
        self.__aplicar()

    @property
    def ctx(self):
        return self.__ctx

    def __aplicar(self):
        geocoders.options.default_ssl_context = self.__ctx