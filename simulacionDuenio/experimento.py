# experimento.py
"""
Gestión de experimentos y réplicas
"""
import pandas as pd
from typing import List, Tuple
from simulador import SimuladorColas
from parametros import ParametrosNegocio

class ExperimentoSimulacion:
    """Gestiona experimentos con múltiples configuraciones y réplicas"""
    
    def __init__(self, params: ParametrosNegocio):
        self.params = params
        self.resultados = []
        
    def ejecutar_experimento(self, configuraciones: List[Tuple[int, int]], callback=None) -> pd.DataFrame:
        """
        Ejecuta experimento para múltiples configuraciones
        configuraciones: lista de tuplas (num_cajas_normales, num_cajas_express)
        callback: función para actualizar progreso en UI
        """
        resultados_totales = []
        total_configs = len(configuraciones)
        
        for config_idx, (num_normal, num_express) in enumerate(configuraciones, 1):
            if callback:
                callback(f"Configuración {config_idx}/{total_configs}: {num_normal}+{num_express} cajas", 
                        (config_idx-1) / total_configs * 100)
            
            replicas_resultados = []
            
            for replica in range(self.params.num_replicas):
                semilla = 1000 * config_idx + replica
                sim = SimuladorColas(num_normal, num_express, self.params, semilla=semilla)
                metricas = sim.simular()
                metricas['replica'] = replica + 1
                replicas_resultados.append(metricas)
                
                if callback and replica % 3 == 0:
                    progreso_config = (replica / self.params.num_replicas) * (100 / total_configs)
                    progreso_total = ((config_idx-1) / total_configs * 100) + progreso_config
                    callback(f"Config {config_idx}/{total_configs} - Réplica {replica+1}/{self.params.num_replicas}", 
                            progreso_total)
            
            df_replicas = pd.DataFrame(replicas_resultados)
            
            resultado_config = {
                'num_cajas_normales': num_normal,
                'num_cajas_express': num_express,
                'num_cajas_total': num_normal + num_express,
                'costo_total_promedio': df_replicas['costo_total'].mean(),
                'costo_total_std': df_replicas['costo_total'].std(),
                'tiempo_sistema_promedio': df_replicas['tiempo_sistema_promedio'].mean(),
                'porcentaje_sla_promedio': df_replicas['porcentaje_sla'].mean(),
                'porcentaje_sla_std': df_replicas['porcentaje_sla'].std(),
                'cumple_sla_pct': (df_replicas['cumple_sla'].sum() / len(df_replicas)) * 100,
                'utilizacion_promedio': df_replicas['utilizacion_promedio'].mean(),
                'clientes_atendidos_promedio': df_replicas['clientes_atendidos'].mean(),
                'costo_cajas_promedio': df_replicas['costo_cajas'].mean(),
                'costo_espera_promedio': df_replicas['costo_espera'].mean(),
                'costo_sla_promedio': df_replicas['costo_sla'].mean(),
            }
            
            resultados_totales.append(resultado_config)
        
        if callback:
            callback("¡Experimento completado!", 100)
        
        return pd.DataFrame(resultados_totales)
