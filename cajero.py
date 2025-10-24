# cajero.py
import random
class Cajero:
    def __init__(self, nombre, tiempo_escaneo, articulos_por_cliente):
        """
        nombre: str -> nombre de la caja
        tiempo_escaneo: float -> segundos por artículo
        articulos_por_cliente: list[int] -> lista con los artículos de cada cliente
        """
        self.nombre = nombre
        self.tiempo_escaneo = tiempo_escaneo
        self.articulos_por_cliente = articulos_por_cliente
        self.personas = len(articulos_por_cliente)

    def calcular_tiempo_cliente(self, articulos):
        """Calcula el tiempo total de atención a un cliente"""
        tiempo_escaneo_total = articulos * self.tiempo_escaneo
        tiempo_cobro = random.randint(15, 30)  # Tiempo variable entre 15 y 30 segundos
        return tiempo_escaneo_total + tiempo_cobro

    def calcular_tiempo_total(self):
        """Suma el tiempo total de todos los clientes en la fila"""
        total = 0
        for articulos in self.articulos_por_cliente:
            total += self.calcular_tiempo_cliente(articulos)
        return total

    def __str__(self):
        return f"{self.nombre}  - Personas: {self.personas}, Escaneo: {self.tiempo_escaneo}s"
