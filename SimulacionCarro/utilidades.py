# utilidades.py
import math

def distancia_angular(a1: float, a2: float) -> float:
    return (a2 - a1) % (2 * math.pi)
