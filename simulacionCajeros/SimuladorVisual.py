import tkinter as tk
import time
import threading
import tkinter.messagebox as messagebox
from simulador import barra_progreso


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    """Dibuja un rectángulo con esquinas redondeadas en el canvas."""
    radius = min(radius, abs(x2 - x1) // 2, abs(y2 - y1) // 2)

    items = []
    items.append(canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, start=90, extent=90, style='pieslice', **kwargs))
    items.append(canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, start=0, extent=90, style='pieslice', **kwargs))
    items.append(canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, start=270, extent=90, style='pieslice', **kwargs))
    items.append(canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, start=180, extent=90, style='pieslice', **kwargs))

    items.append(canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs))
    items.append(canvas.create_rectangle(x1, y1 + radius, x1 + radius, y2 - radius, **kwargs))
    items.append(canvas.create_rectangle(x2 - radius, y1 + radius, x2, y2 - radius, **kwargs))

    return items


class ClienteUI:
    def __init__(self, canvas, x, y, articulos):
        self.canvas = canvas
        self.articulos = articulos
        self.x = x
        self.y = y
        self.emoji = "🙂"
        self.is_moving = False
        
        canvas_bg = canvas.cget('bg') if 'bg' in canvas.keys() else 'white'
        self.bg = canvas.create_oval(x-18, y-18, x+18, y+18, fill=canvas_bg, outline='')
        self.icon = canvas.create_text(x, y, text=self.emoji, font=("Arial", 18, "bold"))
        self.counter = canvas.create_text(x, y + 22, text=f"(0/{articulos})", font=("Arial", 9), fill="#333333")
        self._highlight = False

    def mover_a(self, target_x, target_y=None, steps=20):
        """Mueve el cliente a una posición objetivo de forma suave."""
        if target_y is None:
            target_y = self.y
            
        self.is_moving = True
        dx_total = target_x - self.x
        dy_total = target_y - self.y
        
        for step in range(steps):
            dx = dx_total / steps
            dy = dy_total / steps
            
            try:
                self.canvas.move(self.bg, dx, dy)
                self.canvas.move(self.icon, dx, dy)
                self.canvas.move(self.counter, dx, dy)
                self.x += dx
                self.y += dy
                self.canvas.update()
                time.sleep(0.015)
            except Exception:
                break
        
        self.is_moving = False

    def cambiar_icono(self, emoji):
        self.emoji = emoji
        self.canvas.itemconfig(self.icon, text=self.emoji)

    def actualizar_contador(self, escaneados, total):
        self.canvas.itemconfig(self.counter, text=f"({escaneados}/{total})")

    def set_highlight(self, enabled=True):
        """Resalta o des-resalta este cliente."""
        if enabled:
            try:
                self.canvas.itemconfig(self.bg, fill="#ffef99", outline="#e6c85a")
            except Exception:
                pass
            self._highlight = True
        else:
            try:
                self.canvas.itemconfig(self.bg, fill=self.canvas.cget('bg'), outline='')
            except Exception:
                pass
            self._highlight = False

    def eliminar(self):
        try:
            self.canvas.delete(self.icon)
            self.canvas.delete(self.counter)
            self.canvas.delete(self.bg)
        except Exception:
            pass


class CajaUI:
    def __init__(self, canvas, caja_modelo, fila_y, info_label):
        self.canvas = canvas
        self.caja = caja_modelo
        self.fila_y = fila_y
        self.info = info_label
        self.tiempo_total = 0.0
        self.clientes_atendidos = 0
        self.articulos_totales = 0
        self.lock = threading.Lock()

        # Diseño de caja
        if "Express" in caja_modelo.nombre:
            caja_color = "#ffad99"
            caja_nombre = caja_modelo.nombre
        else:
            caja_color = "#b3e7ff"
            caja_nombre = caja_modelo.nombre

        self.caja_grafica = create_rounded_rectangle(canvas, 50, fila_y, 150, fila_y + 50, radius=12, fill=caja_color, outline="black", width=2)

        if "Express" in caja_modelo.nombre:
            nombre_font = ("Arial", 11, "bold")
            caja_display = caja_nombre.replace("Express", "\nExpress")
        else:
            nombre_font = ("Arial", 14, "bold")
            caja_display = caja_nombre

        canvas.create_text(100, fila_y + 25, text=caja_display, font=nombre_font, fill="black", anchor="center", justify="center")

        # Barra de progreso
        self.progress_boxes = []
        self.block_w = 10
        self.block_h = 10
        self.block_spacing = 4
        self.blocks_y1 = fila_y + 58
        self.blocks_y2 = fila_y + 58 + self.block_h

        # Posiciones de clientes
        self.front_x = 180
        self.spacing_x = 60
        
        self.clientes = [
            ClienteUI(canvas, self.front_x + i*self.spacing_x, fila_y + 25, caja_modelo.articulos_por_cliente[i])
            for i in range(len(caja_modelo.articulos_por_cliente))
        ]
        
        if self.clientes:
            for c in self.clientes:
                c.set_highlight(False)
            self.clientes[-1].set_highlight(True)

    def crear_bloques(self, articulos):
        self.limpiar_bloques()
        if articulos <= 0:
            return
        total_width = articulos * self.block_w + (articulos - 1) * self.block_spacing
        start_x = 100 - total_width/2
        boxes = []
        for i in range(articulos):
            x1 = start_x + i * (self.block_w + self.block_spacing)
            x2 = x1 + self.block_w
            ids = create_rounded_rectangle(self.canvas, x1, self.blocks_y1, x2, self.blocks_y2, radius=3, fill="#ffffff", outline="#aaaaaa")
            boxes.append(ids)
        self.progress_boxes = boxes

    def llenar_bloque(self, idx):
        if 1 <= idx <= len(self.progress_boxes):
            group = self.progress_boxes[idx-1]
            for rect_id in group:
                try:
                    self.canvas.itemconfig(rect_id, fill="#333333", outline="#000000")
                except Exception:
                    pass

    def limpiar_bloques(self):
        for group in getattr(self, 'progress_boxes', []):
            for r in group:
                try:
                    self.canvas.delete(r)
                except Exception:
                    pass
        self.progress_boxes = []

    def avanzar_fila(self):
        """Mueve todos los clientes una posición hacia adelante."""
        with self.lock:
            threads = []
            for idx, cliente in enumerate(self.clientes):
                target_x = self.front_x + idx * self.spacing_x
                t = threading.Thread(target=cliente.mover_a, args=(target_x,))
                t.start()
                threads.append(t)
            
            # Esperar a que terminen todos los movimientos
            for t in threads:
                t.join()
            
            # Actualizar highlights - pintar el último
            for i, c in enumerate(self.clientes):
                c.set_highlight(i == len(self.clientes) - 1)

    def servir_cliente(self, cliente, articulos, tiempos_articulos, tiempo_cobro):
        """Atiende a un cliente: escanea, cobra y anima la salida."""
        try:
            self.crear_bloques(articulos)
            
            # Escaneo
            for i, t_art in enumerate(tiempos_articulos, start=1):
                self.llenar_bloque(i)
                cliente.actualizar_contador(i, articulos)
                time.sleep(0.18)
                try:
                    self.canvas.update()
                except Exception:
                    pass

            # Pago
            cliente.cambiar_icono("💵")
            time.sleep(tiempo_cobro / 32)

            # Volver al icono original antes de irse
            cliente.cambiar_icono("🙂")
            
            # Salida suave
            cliente.mover_a(cliente.x, cliente.y + 40, steps=15)
            cliente.mover_a(cliente.x + 300, cliente.y, steps=20)
            cliente.eliminar()

        finally:
            try:
                self.limpiar_bloques()
            except Exception:
                pass

    def atender(self):
        try:
            self.canvas.delete(getattr(self, 'result_text', None))
        except Exception:
            pass

        while self.clientes:
            with self.lock:
                if not self.clientes:
                    break
                cliente = self.clientes.pop(0)
                articulos = self.caja.articulos_por_cliente[len(self.caja.articulos_por_cliente) - len(self.clientes) - 1]
            
            tiempo_total, tiempos_articulos, tiempo_cobro = self.caja.calcular_tiempo_cliente(articulos)
            
            try:
                self.tiempo_total += float(tiempo_total)
                self.clientes_atendidos += 1
                self.articulos_totales += articulos
            except Exception:
                pass

            # Cambiar icono antes de atender
            cliente.cambiar_icono("🛍️")
            
            # Atender cliente
            self.servir_cliente(cliente, articulos, tiempos_articulos, tiempo_cobro)
            
            # Después de que el cliente se va, avanzar la fila
            if self.clientes:
                self.avanzar_fila()

        # Mostrar tiempo total
        try:
            total_t = float(getattr(self, 'tiempo_total', 0.0))
            mins = int(total_t // 60)
            secs = int(total_t % 60)
            clientes = getattr(self, 'clientes_atendidos', 0)
            articulos = getattr(self, 'articulos_totales', 0)
            texto_linea1 = f"Total: {mins}m {secs}s"
            texto_linea2 = f"{clientes} clientes | {articulos} artículos"
            self.result_text = self.canvas.create_text(100, self.blocks_y1 + self.block_h/2 - 6, text=texto_linea1, font=("Arial", 9, "bold"), fill="#333333")
            self.result_text2 = self.canvas.create_text(100, self.blocks_y1 + self.block_h/2 + 6, text=texto_linea2, font=("Arial", 9), fill="#666666")
            self.canvas.update()
        except Exception:
            pass


def simular_visual(cajas):
    root = tk.Tk()
    root.title("Simulación Visual de Cajas")

    # Scrollable canvas: compute exact total height and show a clipped
    # viewport (up to 6 cajas high). The canvas scrollregion is set to the
    # full content height so the scrollbar can reach all cajas.
    total_height = 150 + len(cajas) * 100
    visible_height = 150 + min(len(cajas), 6) * 100

    # Layout: canvas on the left, results side-frame will be added below
    canvas_container = tk.Frame(root)
    canvas_container.pack(fill='both', expand=True)

    canvas = tk.Canvas(canvas_container, width=1100, height=visible_height, bg="white")
    vsb = tk.Scrollbar(canvas_container, orient='vertical')
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)

    # Título principal
    canvas.create_text(550, 25, text="- SUPERMERCADO -", font=("Arial", 20, "bold"), fill="#2c3e50")
    canvas.create_text(550, 55, text="── Sección de Cajas ──", font=("Arial", 14), fill="#7f8c8d")

    # Compute posiciones and snap targets before creating CajaUI
    posiciones = [130 + i * 100 for i in range(len(cajas))]
    header_height = 90
    snap_targets = [max(0, y - header_height) for y in posiciones]
    max_scroll_px = max(0, total_height - visible_height)

    # Set scrollregion and initial view
    canvas.configure(scrollregion=(0, 0, 1100, total_height))
    canvas.yview_moveto(0)

    # Snapping helpers
    snap_after_id = None

    def snap_to_nearest():
        nonlocal snap_after_id
        snap_after_id = None
        try:
            curr = canvas.canvasy(0)
            nearest = min(snap_targets, key=lambda t: abs(t - curr)) if snap_targets else 0
            target = min(max(0, nearest), max_scroll_px)
            canvas.yview_moveto(target / total_height if total_height > 0 else 0)
        except Exception:
            pass

    def schedule_snap(delay=200):
        nonlocal snap_after_id
        if snap_after_id:
            root.after_cancel(snap_after_id)
        snap_after_id = root.after(delay, snap_to_nearest)

    # Scroll handlers
    def on_vsb_scroll(*args):
        try:
            # Delegate to canvas yview
            canvas.yview(*args)
        except Exception:
            pass
        schedule_snap()

    def _on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        except Exception:
            pass
        schedule_snap()

    vsb.config(command=on_vsb_scroll)
    canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', _on_mousewheel))
    canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))

    # Small info label (kept for compatibility but not used as primary result area)
    info = tk.Label(root, text="", font=("Arial", 14), fg="black", justify="center")
    info.pack(pady=10)

    cajas_ui = [
        CajaUI(canvas, caja, posiciones[i], info)
        for i, caja in enumerate(cajas)
    ]

    simulacion_activa = False

    def iniciar():
        nonlocal simulacion_activa
        if simulacion_activa:
            return

        simulacion_activa = True
        btn_iniciar.config(state='disabled', text="Simulación en curso...")

        threads = []
        for ui in cajas_ui:
            t = threading.Thread(target=ui.atender)
            t.start()
            threads.append(t)

        def watcher():
            nonlocal simulacion_activa
            for t in threads:
                t.join()
            try:
                mejor_ui = min(cajas_ui, key=lambda u: getattr(u, 'tiempo_total', float('inf')))
                mejor_nombre = mejor_ui.caja.nombre
                mejor_t = float(getattr(mejor_ui, 'tiempo_total', 0))
                mins = int(mejor_t // 60)
                secs = int(mejor_t % 60)
                texto = f"Caja más rápida: {mejor_nombre} (≈ {mins} min {secs} s)"
                root.after(0, lambda: info.config(text=texto))
                # Popup to ensure the user sees the result
                root.after(100, lambda: messagebox.showinfo("Mejor caja", f"Caja más rápida: {mejor_nombre}\nTiempo: {mins} min {secs} s"))
            except Exception:
                root.after(0, lambda: info.config(text="Caja más rápida: N/A"))

            simulacion_activa = False
            # simulacion finalizada

        threading.Thread(target=watcher, daemon=True).start()

    # Botón situado en la esquina superior derecha
    btn_iniciar = tk.Button(root, text="Iniciar Simulación", font=("Arial", 14), command=iniciar)
    btn_iniciar.place(relx=1.0, x=-10, y=10, anchor='ne')
    
    
    root.mainloop()


def main():
    """Función principal para configurar y ejecutar la simulación."""
    from simulador import Caja
    
    root = tk.Tk()
    root.title("Configuración de Simulación")
    root.geometry("500x400")
    root.resizable(False, False)
    
    # Frame principal
    main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    # Título
    tk.Label(main_frame, text="🛒 Configuración de Cajas", font=("Arial", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))
    
    # Frame para cajas normales
    frame_normal = tk.Frame(main_frame, bg="white")
    frame_normal.pack(pady=10, fill="x")
    tk.Label(frame_normal, text="Cajas Normales:", font=("Arial", 12), bg="white").pack(side="left", padx=(0, 10))
    spin_normal = tk.Spinbox(frame_normal, from_=0, to=10, width=10, font=("Arial", 12))
    spin_normal.delete(0, "end")
    spin_normal.insert(0, "2")
    spin_normal.pack(side="left")
    
    # Frame para cajas express (fija en 1, no editable)
    frame_express = tk.Frame(main_frame, bg="white")
    frame_express.pack(pady=10, fill="x")
    tk.Label(frame_express, text="Cajas Express:", font=("Arial", 12), bg="white").pack(side="left", padx=(0, 10))
    # Mostramos la express como fija en 1 (por defecto). El usuario solo elige las normales.
    tk.Label(frame_express, text="1 (por defecto)", font=("Arial", 12), bg="white").pack(side="left")
    
    # Información
    info_text = """
    Cajas Normales: Sin límite de artículos
    Cajas Express: Máximo 10 artículos por cliente
    
    Los clientes se distribuirán aleatoriamente.
    """
    tk.Label(main_frame, text=info_text, font=("Arial", 10), bg="white", fg="#666666", justify="left").pack(pady=20)
    
    # Variable para mensaje de error
    error_label = tk.Label(main_frame, text="", font=("Arial", 10), bg="white", fg="red")
    error_label.pack()
    
    def iniciar_simulacion():
        try:
            num_normales = int(spin_normal.get())
            # La cantidad de cajas express está fija en 1 por defecto
            num_express = 1
            
            if num_normales + num_express == 0:
                error_label.config(text="Debe haber al menos una caja")
                return
            
            if num_normales + num_express > 10:
                error_label.config(text="Máximo 10 cajas en total")
                return
            
            # Crear cajas
            cajas = []
            for i in range(num_normales):
                cajas.append(Caja(f"Caja {i+1}"))
            for i in range(num_express):
                cajas.append(Caja(f"Caja Express {i+1}", es_express=True))
            
            # Cerrar ventana de configuración
            root.destroy()
            
            # Iniciar simulación visual
            simular_visual(cajas)
            
        except ValueError:
            error_label.config(text="Por favor ingrese números válidos")
    
    # Botón iniciar
    btn_iniciar = tk.Button(main_frame, text="Iniciar Simulación", font=("Arial", 14, "bold"), 
                           bg="#3498db", fg="white", padx=20, pady=10, command=iniciar_simulacion)
    btn_iniciar.pack(pady=20)
    
    root.mainloop()


