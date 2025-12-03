# visualizador.py
"""
Generación de gráficos y reportes
"""
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd

class GeneradorReportes:
    """Genera visualizaciones y reportes"""
    
    @staticmethod
    def graficar_resultados(df: pd.DataFrame, titulo: str = "Análisis de Configuraciones"):
        """Genera gráficos comparativos"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 9))
        fig.suptitle(titulo, fontsize=16, fontweight='bold')
        
        # Gráfico 1: Costo Total vs Número de Cajas
        ax1 = axes[0, 0]
        ax1.errorbar(df['num_cajas_total'], df['costo_total_promedio'], 
                    yerr=df['costo_total_std'], marker='o', capsize=5, linewidth=2)
        ax1.set_xlabel('Número Total de Cajas')
        ax1.set_ylabel('Costo Total (USD)')
        ax1.set_title('Costo Total vs Número de Cajas')
        ax1.grid(True, alpha=0.3)
        
        idx_min = df['costo_total_promedio'].idxmin()
        ax1.axvline(df.loc[idx_min, 'num_cajas_total'], color='r', 
                   linestyle='--', alpha=0.5, label='Óptimo')
        ax1.legend()
        
        # Gráfico 2: Componentes del Costo
        ax2 = axes[0, 1]
        width = 0.25
        x = np.arange(len(df))
        ax2.bar(x - width, df['costo_cajas_promedio'], width, label='Costo Cajas')
        ax2.bar(x, df['costo_espera_promedio'], width, label='Costo Espera')
        ax2.bar(x + width, df['costo_sla_promedio'], width, label='Penalización SLA')
        ax2.set_xlabel('Configuración (Total Cajas)')
        ax2.set_ylabel('Costo (USD)')
        ax2.set_title('Componentes del Costo')
        ax2.set_xticks(x)
        ax2.set_xticklabels(df['num_cajas_total'])
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Gráfico 3: % SLA vs Número de Cajas
        ax3 = axes[1, 0]
        ax3.errorbar(df['num_cajas_total'], df['porcentaje_sla_promedio'],
                    yerr=df['porcentaje_sla_std'], marker='s', capsize=5, linewidth=2,
                    color='green')
        ax3.axhline(80, color='r', linestyle='--', label='Objetivo SLA (80%)')
        ax3.set_xlabel('Número Total de Cajas')
        ax3.set_ylabel('% Cumplimiento SLA')
        ax3.set_title('Cumplimiento de SLA vs Número de Cajas')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim([0, 105])
        
        # Gráfico 4: Utilización vs Número de Cajas
        ax4 = axes[1, 1]
        ax4.plot(df['num_cajas_total'], df['utilizacion_promedio'],
                marker='^', linewidth=2, markersize=8, color='orange')
        ax4.axhline(0.85, color='r', linestyle='--', alpha=0.5, label='Alta (85%)')
        ax4.axhline(0.70, color='y', linestyle='--', alpha=0.5, label='Media (70%)')
        ax4.set_xlabel('Número Total de Cajas')
        ax4.set_ylabel('Utilización Promedio')
        ax4.set_title('Utilización de Cajas')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim([0, 1.1])
        
        plt.tight_layout()
        filename = f'analisis_cajas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        
        return filename
    
    @staticmethod
    def generar_resumen(df: pd.DataFrame) -> str:
        """Genera resumen de resultados"""
        idx_optimo = df['costo_total_promedio'].idxmin()
        mejor = df.loc[idx_optimo]
        
        resumen = f"""
╔══════════════════════════════════════════════════════════════╗
║                    RESUMEN DE RESULTADOS                     ║
╚══════════════════════════════════════════════════════════════╝

CONFIGURACIÓN ÓPTIMA:
  • {int(mejor['num_cajas_normales'])} cajas normales + {int(mejor['num_cajas_express'])} caja express

COSTOS (día de 8 horas):
  • Total: ${mejor['costo_total_promedio']:.2f} ± ${mejor['costo_total_std']:.2f}
  • Cajas: ${mejor['costo_cajas_promedio']:.2f}
  • Espera: ${mejor['costo_espera_promedio']:.2f}
  • Penalización SLA: ${mejor['costo_sla_promedio']:.2f}

DESEMPEÑO:
  • SLA: {mejor['porcentaje_sla_promedio']:.1f}% ± {mejor['porcentaje_sla_std']:.1f}%
  • Cumplimiento: {mejor['cumple_sla_pct']:.0f}% de réplicas
  • Utilización: {mejor['utilizacion_promedio']:.1%}
  • Tiempo en sistema: {mejor['tiempo_sistema_promedio']:.2f} min
  • Clientes atendidos: {mejor['clientes_atendidos_promedio']:.0f}

═══════════════════════════════════════════════════════════════

REGLA DE APERTURA PROPUESTA:

Abrir caja adicional si se cumplen 2+ de:
  1. Utilización > 85% (ventana 15 min)
  2. Tiempo espera > 5 min (últimos 20 clientes)
  3. Cola > {int(mejor['num_cajas_total'] * 2)} clientes
  4. SLA < 80% (últimos 30 clientes)

═══════════════════════════════════════════════════════════════
"""
        return resumen
