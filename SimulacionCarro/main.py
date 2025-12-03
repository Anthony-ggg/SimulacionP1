# main.py
from generadorVehiculos import generar_vehiculos
from simulacion import SimulacionRedondel
from interfaz import InterfazRedondel

def main():
    # --- CONFIGURACIÓN DE LA SIMULACIÓN ---
    
    # RADIO: Define el tamaño del redondel en metros.
    # Recuerda: Longitud Vuelta = 2 * 3.1416 * radio.
    # Ej: Si radio=8, vuelta=50m. Si radio=16, vuelta=100m.
    radio = 6.0

    # VELOCIDAD: Metros por segundo.
    # Para saber km/h mentalmente, multiplica esto por 3.6.
    # Ej: 2.0 m/s = 7.2 km/h (velocidad de paseo/parking).
    velocidad_fija = 3.0
    
    # DISTANCIA DE SEGURIDAD: Espacio mínimo (metros) para no chocar.
    distancia_seguridad = 3.0
    
    dt = 0.05
    
    vehiculos = generar_vehiculos(
        n_min=1,
        n_max=1,
        radio=radio,
        velocidad=velocidad_fija,
        distancia_seguridad=5.0 
    )

    sim = SimulacionRedondel(
        vehiculos,
        radio=radio,
        distancia_seguridad=distancia_seguridad,
        dt=dt,
        velocidad_estandar=velocidad_fija
    )

    interfaz = InterfazRedondel(sim)
    interfaz.loop()

if __name__ == "__main__":
    main()