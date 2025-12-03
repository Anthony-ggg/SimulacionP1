# parametros.py
"""
Parámetros de configuración del negocio
"""
from dataclasses import dataclass

@dataclass
class ParametrosNegocio:
    """Parámetros de costos y objetivos de servicio"""
    c_caja: float = 0.50  # USD/min por caja activa
    c_espera: float = 0.10  # USD/min por cliente esperando
    c_SLA: float = 5.0  # USD por cada punto porcentual de incumplimiento
    
    sla_porcentaje: float = 80.0  # 80% de clientes
    sla_tiempo_max: float = 8.0  # 8 minutos
    
    tiempo_simulacion: int = 480  # minutos (8 horas)
    num_replicas: int = 15
    
    lambda_hora: float = 60.0  # 60 clientes por hora
    
    def get_lambda_min(self):
        return self.lambda_hora / 60.0
