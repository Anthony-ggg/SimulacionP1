# cajero_express.py
from cajero import Cajero

class CajeroExpress(Cajero):
    def __init__(self, nombre, tiempo_escaneo, articulos_por_cliente):
        super().__init__(nombre, tiempo_escaneo, articulos_por_cliente)
        self.limite_articulos = 10

    def calcular_tiempo_cliente(self, articulos):
        """Limita los artículos si exceden el máximo permitido"""
        if articulos > self.limite_articulos:
            articulos = self.limite_articulos
        tiempo_escaneo_total = articulos * self.tiempo_escaneo
        tiempo_cobro = 20
        return tiempo_escaneo_total + tiempo_cobro

    def __str__(self):
        return f"{self.nombre} (Express) - Personas: {self.personas}, Escaneo: {self.tiempo_escaneo}s"
