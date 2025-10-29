# cajero.py
import random
class Cajero:
    def __init__(self, nombre, articulos_por_cliente):
        """
        nombre: str -> nombre de la caja
        tiempo_escaneo: float -> segundos por artículo
        articulos_por_cliente: list[int] -> lista con los artículos de cada cliente
        """
        self.nombre = nombre
        
        self.articulos_por_cliente = articulos_por_cliente
        self.personas = len(articulos_por_cliente)

    def calcular_tiempo_cliente(self, articulos):
    #Calcualr cada tiempo de cliente
        
        # Guardar tiempo por cada artículo
        tiempos_articulos = [random.randint(5, 9) for _ in range(articulos)]
        tiempo_escaneo_total = sum(tiempos_articulos)

        tiempo_cobro = random.randint(15, 30)  # Tiempo de cobro variable entre 15 y 30 segundos

        #tiempo total de atencion al cliente
        tiempo_total = tiempo_escaneo_total + tiempo_cobro
        return tiempo_total, tiempos_articulos, tiempo_cobro

    def calcular_tiempo_total(self):
        """Suma el tiempo total de todos los clientes en la fila"""
        total = 0
        for articulos in self.articulos_por_cliente:
            tiempo_total, _,_ = self.calcular_tiempo_cliente(articulos)
            total += tiempo_total
        return total

    def __str__(self):
        return f"{self.nombre}  - Personas: {self.personas}"
