# modelos.py
"""
Clases del modelo de simulación
"""
import random
import numpy as np

class Cliente:
    """Representa un cliente en el sistema"""
    id_counter = 0
    
    def __init__(self, tiempo_llegada: float, num_articulos: int):
        Cliente.id_counter += 1
        self.id = Cliente.id_counter
        self.tiempo_llegada = tiempo_llegada
        self.num_articulos = num_articulos
        self.tiempo_inicio_servicio = None
        self.tiempo_fin_servicio = None
        
    def get_tiempo_espera(self) -> float:
        if self.tiempo_inicio_servicio is None:
            return 0.0
        return self.tiempo_inicio_servicio - self.tiempo_llegada
    
    def get_tiempo_servicio(self) -> float:
        if self.tiempo_fin_servicio is None or self.tiempo_inicio_servicio is None:
            return 0.0
        return self.tiempo_fin_servicio - self.tiempo_inicio_servicio
    
    def get_tiempo_sistema(self) -> float:
        if self.tiempo_fin_servicio is None:
            return 0.0
        return self.tiempo_fin_servicio - self.tiempo_llegada


class Caja:
    """Representa una caja registradora"""
    
    def __init__(self, id_caja: int, es_express: bool = False):
        self.id = id_caja
        self.es_express = es_express
        self.limite_articulos = 10 if es_express else float('inf')
        self.tiempo_ocupado = 0.0
        self.clientes_atendidos = 0
        self.cliente_actual = None
        self.tiempo_finalizacion = 0.0
        
    def puede_atender(self, cliente: Cliente) -> bool:
        return cliente.num_articulos <= self.limite_articulos
    
    def esta_libre(self, tiempo_actual: float) -> bool:
        return tiempo_actual >= self.tiempo_finalizacion
    
    def iniciar_servicio(self, cliente: Cliente, tiempo_actual: float) -> float:
        cliente.tiempo_inicio_servicio = tiempo_actual
        
        tiempo_escaneo = sum([random.uniform(5/60, 9/60) for _ in range(cliente.num_articulos)])
        
        if self.es_express:
            tiempo_cobro = 20/60
        else:
            tiempo_cobro = random.uniform(15/60, 30/60)
        
        tiempo_servicio = tiempo_escaneo + tiempo_cobro
        
        self.cliente_actual = cliente
        self.tiempo_finalizacion = tiempo_actual + tiempo_servicio
        cliente.tiempo_fin_servicio = self.tiempo_finalizacion
        
        self.tiempo_ocupado += tiempo_servicio
        self.clientes_atendidos += 1
        
        return tiempo_servicio
    
    def get_utilizacion(self, tiempo_total: float) -> float:
        if tiempo_total <= 0:
            return 0.0
        return self.tiempo_ocupado / tiempo_total
