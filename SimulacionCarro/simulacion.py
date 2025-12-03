# simulacion.py
from logica import calcular_detenciones, ordenar_por_angulo
from entidades import Vehiculo
from utilidades import distancia_angular
import math
import random

class SimulacionRedondel:
    def __init__(self, vehiculos, radio, distancia_seguridad, dt, velocidad_estandar):
        self.vehiculos = vehiculos
        self.radio = radio
        self.distancia_seguridad = distancia_seguridad
        self.dt = dt
        self.velocidad_estandar = velocidad_estandar
        self.tiempo_actual = 0.0
        # NOTA: Ya no necesitamos self.id_counter, lo calcularemos dinámicamente

    def paso(self):
        detenciones = calcular_detenciones(
            self.vehiculos,
            self.radio,
            self.distancia_seguridad
        )

        for v, detener_trafico in zip(self.vehiculos, detenciones):
            v.actualizar_estado(detener_trafico)
            v.avanzar(self.dt)

        self.tiempo_actual += self.dt

    def toggle_freno_manual(self, vehiculo_id):
        for v in self.vehiculos:
            if v.id == vehiculo_id:
                v.freno_manual = not v.freno_manual
                break

    def frenar_aleatorio(self):
        candidatos = [v for v in self.vehiculos if not v.freno_manual]
        if candidatos:
            elegido = random.choice(candidatos)
            elegido.freno_manual = True
            return elegido.id
        return None

    def liberar_todos(self):
        for v in self.vehiculos:
            v.freno_manual = False

    def eliminar_vehiculo(self):
        if self.vehiculos:
            self.vehiculos.pop() # Elimina el último de la lista y libera su ID
            return True
        return False

    def cambiar_distancia_seguridad(self, delta):
        self.distancia_seguridad = max(1.0, self.distancia_seguridad + delta)

    def intentar_agregar_vehiculo(self):
        # CASO 0 CARROS:
        if not self.vehiculos:
            self._crear_auto_en(0.0)
            return True

        # CASO 1 CARRO:
        if len(self.vehiculos) == 1:
            angulo_actual = self.vehiculos[0].angulo
            angulo_nuevo = (angulo_actual + math.pi) % (2 * math.pi)
            self._crear_auto_en(angulo_nuevo)
            return True

        # CASO 2+ CARROS:
        ordenados = ordenar_por_angulo(self.vehiculos)
        n = len(ordenados)
        
        max_gap_rad = 0.0
        mejor_angulo_inicio = 0.0

        for i in range(n):
            v_actual = ordenados[i]
            v_siguiente = ordenados[(i + 1) % n]
            
            gap = distancia_angular(v_actual.angulo, v_siguiente.angulo)
            
            if gap > max_gap_rad:
                max_gap_rad = gap
                mejor_angulo_inicio = v_actual.angulo

        espacio_metros = max_gap_rad * self.radio
        espacio_minimo_requerido = self.distancia_seguridad * 2.2 

        if espacio_metros >= espacio_minimo_requerido:
            angulo_nuevo = (mejor_angulo_inicio + max_gap_rad / 2) % (2 * math.pi)
            self._crear_auto_en(angulo_nuevo)
            return True
        else:
            return False

    def _crear_auto_en(self, angulo):
        """
        Crea un auto reciclando los IDs.
        Busca el número más bajo (0, 1, 2...) que no esté usándose.
        """
        # 1. Obtenemos todos los IDs que existen actualmente en la pista
        ids_usados = {v.id for v in self.vehiculos}
        
        # 2. Buscamos el primer número libre empezando desde 0
        nuevo_id = 0
        while nuevo_id in ids_usados:
            nuevo_id += 1
            
        # 3. Creamos el auto con ese ID reciclado
        nuevo_auto = Vehiculo(
            id=nuevo_id,
            angulo=angulo,
            velocidad=self.velocidad_estandar,
            radio=self.radio
        )
        self.vehiculos.append(nuevo_auto)