# main.py
"""
Interfaz gráfica principal para la simulación
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from parametros import ParametrosNegocio
from experimento import ExperimentoSimulacion
from visualizador import GeneradorReportes
import pandas as pd

class SimulacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Cajas - Enfoque de Negocio")
        self.root.geometry("1200x700")
        
        self.params = ParametrosNegocio()
        self.df_resultados = None
        self.simulacion_activa = False
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal dividido
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Configuración
        left_frame = ttk.LabelFrame(main_frame, text="⚙️ Configuración", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        # Parámetros de costos
        ttk.Label(left_frame, text="💰 COSTOS", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(left_frame, text="Costo caja ($/min):").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_c_caja = ttk.Entry(left_frame, width=10)
        self.entry_c_caja.insert(0, "0.50")
        self.entry_c_caja.grid(row=1, column=1, pady=2)
        
        ttk.Label(left_frame, text="Costo espera ($/min):").grid(row=2, column=0, sticky='w', pady=2)
        self.entry_c_espera = ttk.Entry(left_frame, width=10)
        self.entry_c_espera.insert(0, "0.10")
        self.entry_c_espera.grid(row=2, column=1, pady=2)
        
        ttk.Label(left_frame, text="Penalización SLA ($/punto):").grid(row=3, column=0, sticky='w', pady=2)
        self.entry_c_sla = ttk.Entry(left_frame, width=10)
        self.entry_c_sla.insert(0, "5.0")
        self.entry_c_sla.grid(row=3, column=1, pady=2)
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Parámetros de servicio
        ttk.Label(left_frame, text="📊 SERVICIO", font=('Arial', 10, 'bold')).grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Label(left_frame, text="Objetivo SLA (%):").grid(row=6, column=0, sticky='w', pady=2)
        self.entry_sla_pct = ttk.Entry(left_frame, width=10)
        self.entry_sla_pct.insert(0, "80")
        self.entry_sla_pct.grid(row=6, column=1, pady=2)
        
        ttk.Label(left_frame, text="Tiempo máx SLA (min):").grid(row=7, column=0, sticky='w', pady=2)
        self.entry_sla_tiempo = ttk.Entry(left_frame, width=10)
        self.entry_sla_tiempo.insert(0, "8.0")
        self.entry_sla_tiempo.grid(row=7, column=1, pady=2)
        
        ttk.Label(left_frame, text="Llegadas (clientes/h):").grid(row=8, column=0, sticky='w', pady=2)
        self.entry_lambda = ttk.Entry(left_frame, width=10)
        self.entry_lambda.insert(0, "60")
        self.entry_lambda.grid(row=8, column=1, pady=2)
        
        ttk.Separator(left_frame, orient='horizontal').grid(row=9, column=0, columnspan=2, sticky='ew', pady=10)
        
        # Parámetros de simulación
        ttk.Label(left_frame, text="⏱️ SIMULACIÓN", font=('Arial', 10, 'bold')).grid(row=10, column=0, columnspan=2, pady=5)
        
        ttk.Label(left_frame, text="Tiempo (min):").grid(row=11, column=0, sticky='w', pady=2)
        self.entry_tiempo = ttk.Entry(left_frame, width=10)
        self.entry_tiempo.insert(0, "480")
        self.entry_tiempo.grid(row=11, column=1, pady=2)
        
        ttk.Label(left_frame, text="Réplicas:").grid(row=12, column=0, sticky='w', pady=2)
        self.entry_replicas = ttk.Entry(left_frame, width=10)
        self.entry_replicas.insert(0, "15")
        self.entry_replicas.grid(row=12, column=1, pady=2)
        
        # Botones
        ttk.Separator(left_frame, orient='horizontal').grid(row=13, column=0, columnspan=2, sticky='ew', pady=10)
        
        self.btn_iniciar = ttk.Button(left_frame, text="▶️ Iniciar Simulación", command=self.iniciar_simulacion)
        self.btn_iniciar.grid(row=14, column=0, columnspan=2, pady=5, sticky='ew')
        
        self.btn_graficar = ttk.Button(left_frame, text="📊 Ver Gráficos", command=self.mostrar_graficos, state='disabled')
        self.btn_graficar.grid(row=15, column=0, columnspan=2, pady=5, sticky='ew')
        
        self.btn_exportar = ttk.Button(left_frame, text="💾 Exportar CSV", command=self.exportar_csv, state='disabled')
        self.btn_exportar.grid(row=16, column=0, columnspan=2, pady=5, sticky='ew')
        
        # Panel derecho - Resultados
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Barra de progreso
        progress_frame = ttk.Frame(right_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.label_progreso = ttk.Label(progress_frame, text="Listo para iniciar simulación")
        self.label_progreso.pack(side=tk.LEFT)
        
        self.progressbar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progressbar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Área de resultados
        results_frame = ttk.LabelFrame(right_frame, text="📋 Resultados", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_resultados = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, 
                                                         font=('Courier', 9))
        self.text_resultados.pack(fill=tk.BOTH, expand=True)
        
    def actualizar_progreso(self, mensaje, progreso):
        self.label_progreso.config(text=mensaje)
        self.progressbar['value'] = progreso
        self.root.update_idletasks()
        
    def iniciar_simulacion(self):
        if self.simulacion_activa:
            return
        
        try:
            # Leer parámetros
            self.params.c_caja = float(self.entry_c_caja.get())
            self.params.c_espera = float(self.entry_c_espera.get())
            self.params.c_SLA = float(self.entry_c_sla.get())
            self.params.sla_porcentaje = float(self.entry_sla_pct.get())
            self.params.sla_tiempo_max = float(self.entry_sla_tiempo.get())
            self.params.lambda_hora = float(self.entry_lambda.get())
            self.params.tiempo_simulacion = int(self.entry_tiempo.get())
            self.params.num_replicas = int(self.entry_replicas.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
            return
        
        self.simulacion_activa = True
        self.btn_iniciar.config(state='disabled')
        self.text_resultados.delete(1.0, tk.END)
        
        # Configuraciones a evaluar
        configuraciones = [
            (1, 1),
            (2, 1),
            (3, 1),
            (4, 1),
            (5, 1),
            (2, 2),
            (3, 2),
        ]
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.ejecutar_experimento, args=(configuraciones,))
        thread.daemon = True
        thread.start()
        
    def ejecutar_experimento(self, configuraciones):
        try:
            experimento = ExperimentoSimulacion(self.params)
            self.df_resultados = experimento.ejecutar_experimento(
                configuraciones, 
                callback=self.actualizar_progreso
            )
            
            # Mostrar resultados
            self.root.after(0, self.mostrar_resultados)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error en simulación: {str(e)}"))
        finally:
            self.simulacion_activa = False
            self.root.after(0, lambda: self.btn_iniciar.config(state='normal'))
            
    def mostrar_resultados(self):
        self.text_resultados.delete(1.0, tk.END)
        
        # Generar tabla
        tabla = "\n" + "=" * 100 + "\n"
        tabla += "RESULTADOS DE LA SIMULACIÓN\n"
        tabla += "=" * 100 + "\n"
        tabla += f"{'Config':<10} {'Cajas':<12} {'Costo Total':<20} {'SLA %':<15} {'Utilización':<15}\n"
        tabla += f"{'':10} {'N+E':<12} {'(USD ± σ)':<20} {'(% ± σ)':<15} {'(%)':<15}\n"
        tabla += "-" * 100 + "\n"
        
        idx_min = self.df_resultados['costo_total_promedio'].idxmin()
        
        for idx, row in self.df_resultados.iterrows():
            config = f"#{idx+1}"
            cajas = f"{int(row['num_cajas_normales'])}+{int(row['num_cajas_express'])}"
            costo = f"${row['costo_total_promedio']:.2f}±{row['costo_total_std']:.2f}"
            sla = f"{row['porcentaje_sla_promedio']:.1f}±{row['porcentaje_sla_std']:.1f}"
            util = f"{row['utilizacion_promedio']:.1%}"
            
            prefijo = ">>> " if idx == idx_min else "    "
            tabla += f"{prefijo}{config:<10} {cajas:<12} {costo:<20} {sla:<15} {util:<15}\n"
        
        tabla += "=" * 100 + "\n"
        
        # Agregar resumen
        generador = GeneradorReportes()
        resumen = generador.generar_resumen(self.df_resultados)
        
        self.text_resultados.insert(tk.END, tabla)
        self.text_resultados.insert(tk.END, resumen)
        
        # Habilitar botones
        self.btn_graficar.config(state='normal')
        self.btn_exportar.config(state='normal')
        
        messagebox.showinfo("Completado", "¡Simulación completada exitosamente!")
        
    def mostrar_graficos(self):
        if self.df_resultados is None:
            return
        
        generador = GeneradorReportes()
        filename = generador.graficar_resultados(self.df_resultados)
        
        messagebox.showinfo("Gráficos", f"Gráficos guardados en:\n{filename}")
        plt.show()
        
    def exportar_csv(self):
        if self.df_resultados is None:
            return
        
        filename = 'resultados_simulacion.csv'
        self.df_resultados.to_csv(filename, index=False)
        messagebox.showinfo("Exportado", f"Resultados exportados a:\n{filename}")

def main():
    root = tk.Tk()
    app = SimulacionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
