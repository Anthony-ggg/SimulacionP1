# interfaz.py
import pygame
import math
from entidades import EstadoVehiculo

class InterfazRedondel:
    def __init__(self, simulacion):
        pygame.init()
        self.sim = simulacion
        
        # --- CAMBIO AQUÍ ---
        # Antes teníamos (0, 0). Ahora ponemos (1000, 800) para un tamaño inicial cómodo.
        # Mantenemos pygame.RESIZABLE para que tengas los botones de minimizar/maximizar.
        self.pantalla = pygame.display.set_mode((1300, 700), pygame.RESIZABLE)
        
        pygame.display.set_caption("Simulación de Vehículos - Ventana Normal")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Consolas", 16)

        # Obtenemos las dimensiones actuales (que serán 1000x800 al inicio)
        self.ancho, self.alto = self.pantalla.get_size()
        self.cx = self.ancho // 2
        self.cy = self.alto // 2
        self.escala = 30 

        # --- BOTONES ---
        # Los bajamos a Y=260
        self.btn_frenar_random = pygame.Rect(10, 260, 200, 30)
        self.btn_liberar_todos = pygame.Rect(10, 300, 200, 30)

    def dibujar_info(self):
        # 1. Cálculos
        perimetro = 2 * math.pi * self.sim.radio
        vel_kmh = self.sim.velocidad_estandar * 3.6

        # 2. Texto Izquierda
        textos_izq = [
            f"--- ESTADO ({len(self.sim.vehiculos)} Carros) ---",
            f"Dist. Seguridad: {self.sim.distancia_seguridad:.1f} m",
            "(Cambiar: Flechas ARRIBA/ABAJO)",
            "",
            "--- TECLAS (Vehiculos)---",
            "[A] Agregar   [E] Eliminar",
            "",
            "",
            "",
            "",
            "",
            "Botones:"
        ]

        y_izq = 10
        for linea in textos_izq:
            img = self.fuente.render(linea, True, (0, 0, 0))
            self.pantalla.blit(img, (10, y_izq))
            y_izq += 20

        # 3. Texto Derecha (Datos Pista)
        textos_der = [
            "--- DATOS PISTA ---",
            f"Radio: {self.sim.radio} m",
            f"Longitud: {perimetro:.2f} m",
            f"Velocidad: {self.sim.velocidad_estandar} m/s",
            f"({vel_kmh:.1f} km/h)"
        ]

        # Se ajusta a la derecha automáticamente
        x_der = self.ancho - 220 
        y_der = 10
        
        for linea in textos_der:
            img = self.fuente.render(linea, True, (0, 0, 0))
            self.pantalla.blit(img, (x_der, y_der))
            y_der += 20

    def dibujar_botones(self):
        # Botón Frenar
        pygame.draw.rect(self.pantalla, (200, 50, 50), self.btn_frenar_random)
        txt1 = self.fuente.render("APLICAR FRENOS", True, (255, 255, 255))
        self.pantalla.blit(txt1, (self.btn_frenar_random.x + 25, self.btn_frenar_random.y + 8))

        # Botón Liberar
        pygame.draw.rect(self.pantalla, (50, 200, 50), self.btn_liberar_todos)
        txt2 = self.fuente.render("QUITAR FRENOS", True, (0, 0, 0))
        self.pantalla.blit(txt2, (self.btn_liberar_todos.x + 35, self.btn_liberar_todos.y + 8))

    def detectar_clic_vehiculo(self, pos_mouse):
        mx, my = pos_mouse
        for v in self.sim.vehiculos:
            vx = self.cx + math.cos(v.angulo) * v.radio * self.escala
            vy = self.cy + math.sin(v.angulo) * v.radio * self.escala
            if math.hypot(mx - vx, my - vy) < 15:
                return v.id
        return None

    def loop(self):
        corriendo = True
        while corriendo:
            # 1. EVENTOS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                
                # Al cambiar tamaño, recalculamos el centro
                elif event.type == pygame.VIDEORESIZE:
                    self.ancho, self.alto = event.w, event.h
                    self.cx = self.ancho // 2
                    self.cy = self.alto // 2
                    self.pantalla = pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if not self.sim.intentar_agregar_vehiculo():
                            print("¡Lleno!")
                    elif event.key == pygame.K_e:
                        self.sim.eliminar_vehiculo()
                    elif event.key == pygame.K_UP:
                        self.sim.cambiar_distancia_seguridad(0.5)
                    elif event.key == pygame.K_DOWN:
                        self.sim.cambiar_distancia_seguridad(-0.5)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = event.pos
                        if self.btn_frenar_random.collidepoint(pos):
                            self.sim.frenar_aleatorio()
                        elif self.btn_liberar_todos.collidepoint(pos):
                            self.sim.liberar_todos()
                        else:
                            id_v = self.detectar_clic_vehiculo(pos)
                            if id_v is not None:
                                self.sim.toggle_freno_manual(id_v)

            # 2. FÍSICA
            self.sim.paso()

            # 3. DIBUJAR
            self.pantalla.fill((255, 255, 255))
            
            # Carretera
            pygame.draw.circle(self.pantalla, (220, 220, 220), (self.cx, self.cy), int(self.sim.radio * self.escala) + 10, 20)
            
            # Vehículos
            for v in self.sim.vehiculos:
                x = self.cx + math.cos(v.angulo) * v.radio * self.escala
                y = self.cy + math.sin(v.angulo) * v.radio * self.escala
                
                if v.freno_manual:
                    color = (255, 200, 0)
                elif v.estado == EstadoVehiculo.DETENIDO:
                    color = (255, 50, 50)
                else:
                    color = (0, 100, 255)

                pygame.draw.circle(self.pantalla, color, (int(x), int(y)), 10)
                lbl = self.fuente.render(str(v.id), True, (0, 0, 0))
                self.pantalla.blit(lbl, (int(x)-5, int(y)-25))

            self.dibujar_info()
            self.dibujar_botones()
            
            pygame.display.update()
            self.reloj.tick(60)

        pygame.quit()