# generadorVehiculos.py
import random
import math
from entidades import Vehiculo
from utilidades import distancia_angular

def generar_vehiculos(
        n_min: int,
        n_max: int,
        radio: float,
        velocidad: float,  # <--- CAMBIO: Una sola velocidad fija
        distancia_seguridad: float
    ):
    
    cantidad = random.randint(n_min, n_max)
    vehiculos = []
    angulos_ocupados = []

    for i in range(cantidad):
        # Lógica para no superponerse al inicio
        while True:
            ang = random.uniform(0, 2 * math.pi)
            valido = True
            for a in angulos_ocupados:
                if distancia_angular(ang, a) * radio < distancia_seguridad:
                    valido = False
                    break
            if valido:
                angulos_ocupados.append(ang)
                break

        # Todos creados con la misma velocidad exacta
        vehiculos.append(
            Vehiculo(
                id=i,
                angulo=ang,
                velocidad=velocidad, # <--- Asignación fija
                radio=radio
            )
        )

    return vehiculos