# cajero_express.py
from cajero import Cajero, random

class CajeroExpress(Cajero):
    def __init__(self, nombre, articulos_por_cliente):
        # Filtramos solo clientes con <= 10 artículos
        articulos_filtrados = [a for a in articulos_por_cliente if a <= 10]
        super().__init__(nombre, articulos_filtrados)
        self.limite_articulos = 10

    def calcular_tiempo_cliente(self, articulos):

        # Tiempo por cada artículo: entre 5 y 9 segundos
        tiempos_articulos = [random.randint(5, 9) for _ in range(articulos)]
        tiempo_escaneo_total = sum(tiempos_articulos)

        tiempo_cobro = 20 #Tiempo de conro fijo

        tiempo_total = tiempo_escaneo_total + tiempo_cobro
        return tiempo_total, tiempos_articulos, tiempo_cobro

    def __str__(self):
        return f"{self.nombre} (Express) - Personas: {self.personas}"
