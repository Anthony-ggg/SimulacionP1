# control.py
def detener_vehiculo(sim: "Simulacion", id_objetivo):
    for v in sim.vehiculos:
        if v.id == id_objetivo:
            v.detener()
