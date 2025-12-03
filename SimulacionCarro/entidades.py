# entidades.py
import math
from dataclasses import dataclass, field
from enum import Enum

class EstadoVehiculo(Enum):
    MOVIENDO = "moviendo"
    DETENIDO = "detenido"

@dataclass
class Vehiculo:
    id: int
    angulo: float
    velocidad: float      # m/s
    radio: float          # metros
    estado: EstadoVehiculo = EstadoVehiculo.MOVIENDO
    # Nuevo: permite forzar la detención desde la interfaz
    freno_manual: bool = False 

    def avanzar(self, dt: float):
        # Solo avanza si no está detenido por tráfico Y no tiene el freno manual puesto
        if self.estado == EstadoVehiculo.MOVIENDO and not self.freno_manual:
            distancia = self.velocidad * dt
            incremento = distancia / self.radio
            self.angulo = (self.angulo + incremento) % (2 * math.pi)

    def actualizar_estado(self, debe_frenar_por_trafico: bool):
        # El estado es DETENIDO si hay tráfico O si el usuario activó el freno manual
        if debe_frenar_por_trafico or self.freno_manual:
            self.estado = EstadoVehiculo.DETENIDO
        else:
            self.estado = EstadoVehiculo.MOVIENDO