# simulador.py
"""
Motor de simulación de eventos discretos
"""
import random
import numpy as np
from typing import List, Dict
from modelos import Cliente, Caja
from parametros import ParametrosNegocio

class SimuladorColas:
    """Simulador de sistema de colas M/M/s"""
    
    def __init__(self, num_cajas: int, num_cajas_express: int, params: ParametrosNegocio, semilla: int = None):
        self.params = params
        self.num_cajas = num_cajas
        self.num_cajas_express = num_cajas_express
        
        if semilla is not None:
            random.seed(semilla)
            np.random.seed(semilla)
        
        self.cajas: List[Caja] = []
        for i in range(num_cajas):
            self.cajas.append(Caja(i+1, es_express=False))
        for i in range(num_cajas_express):
            self.cajas.append(Caja(num_cajas+i+1, es_express=True))
        
        self.cola: List[Cliente] = []
        self.clientes_completados: List[Cliente] = []
        self.tiempo_actual = 0.0
        self.clientes_generados = 0
        
    def generar_cliente(self, tiempo: float) -> Cliente:
        if random.random() < 0.4:
            num_articulos = random.randint(1, 5)
        elif random.random() < 0.7:
            num_articulos = random.randint(6, 10)
        else:
            num_articulos = random.randint(11, 25)
        
        self.clientes_generados += 1
        return Cliente(tiempo, num_articulos)
    
    def asignar_caja(self, cliente: Cliente) -> Caja:
        cajas_disponibles = [c for c in self.cajas 
                            if c.esta_libre(self.tiempo_actual) and c.puede_atender(cliente)]
        
        if not cajas_disponibles:
            return None
        
        cajas_express = [c for c in cajas_disponibles if c.es_express]
        if cajas_express and cliente.num_articulos <= 10:
            return cajas_express[0]
        
        return cajas_disponibles[0]
    
    def simular(self) -> Dict:
        Cliente.id_counter = 0
        tiempo_fin = self.params.tiempo_simulacion
        lambda_min = self.params.get_lambda_min()
        
        tiempos_llegada = []
        t = 0
        while t < tiempo_fin:
            t += np.random.exponential(1/lambda_min)
            if t < tiempo_fin:
                tiempos_llegada.append(t)
        
        for tiempo_llegada in tiempos_llegada:
            self.tiempo_actual = tiempo_llegada
            cliente = self.generar_cliente(tiempo_llegada)
            
            caja = self.asignar_caja(cliente)
            
            if caja is not None:
                caja.iniciar_servicio(cliente, self.tiempo_actual)
                self.clientes_completados.append(cliente)
            else:
                self.cola.append(cliente)
        
        while self.cola:
            proximos_eventos = [c.tiempo_finalizacion for c in self.cajas 
                              if c.tiempo_finalizacion > self.tiempo_actual]
            
            if not proximos_eventos:
                break
            
            self.tiempo_actual = min(proximos_eventos)
            
            clientes_procesados = []
            for cliente in self.cola:
                caja = self.asignar_caja(cliente)
                if caja is not None:
                    caja.iniciar_servicio(cliente, self.tiempo_actual)
                    self.clientes_completados.append(cliente)
                    clientes_procesados.append(cliente)
            
            for cliente in clientes_procesados:
                self.cola.remove(cliente)
            
            if self.tiempo_actual > tiempo_fin + 60:
                break
        
        return self.calcular_metricas()
    
    def calcular_metricas(self) -> Dict:
        if not self.clientes_completados:
            return self._metricas_vacias()
        
        tiempos_sistema = [c.get_tiempo_sistema() for c in self.clientes_completados]
        tiempos_espera = [c.get_tiempo_espera() for c in self.clientes_completados]
        
        clientes_dentro_sla = sum(1 for t in tiempos_sistema if t <= self.params.sla_tiempo_max)
        porcentaje_sla = (clientes_dentro_sla / len(self.clientes_completados)) * 100
        
        utilizaciones = [c.get_utilizacion(self.params.tiempo_simulacion) for c in self.cajas]
        
        costo_cajas = self.params.c_caja * len(self.cajas) * self.params.tiempo_simulacion
        costo_espera = self.params.c_espera * sum(tiempos_sistema)
        incumplimiento_sla = max(0, self.params.sla_porcentaje - porcentaje_sla)
        costo_sla = self.params.c_SLA * incumplimiento_sla
        costo_total = costo_cajas + costo_espera + costo_sla
        
        return {
            'num_cajas_total': len(self.cajas),
            'num_cajas_normales': self.num_cajas,
            'num_cajas_express': self.num_cajas_express,
            'clientes_atendidos': len(self.clientes_completados),
            'tiempo_sistema_promedio': np.mean(tiempos_sistema),
            'tiempo_espera_promedio': np.mean(tiempos_espera),
            'porcentaje_sla': porcentaje_sla,
            'cumple_sla': porcentaje_sla >= self.params.sla_porcentaje,
            'utilizacion_promedio': np.mean(utilizaciones),
            'costo_cajas': costo_cajas,
            'costo_espera': costo_espera,
            'costo_sla': costo_sla,
            'costo_total': costo_total,
        }
    
    def _metricas_vacias(self) -> Dict:
        return {
            'num_cajas_total': len(self.cajas),
            'num_cajas_normales': self.num_cajas,
            'num_cajas_express': self.num_cajas_express,
            'clientes_atendidos': 0,
            'tiempo_sistema_promedio': 0,
            'tiempo_espera_promedio': 0,
            'porcentaje_sla': 0,
            'cumple_sla': False,
            'utilizacion_promedio': 0,
            'costo_cajas': 0,
            'costo_espera': 0,
            'costo_sla': 0,
            'costo_total': 0,
        }
