# logica.py

from utilidades import distancia_angular

def ordenar_por_angulo(vehiculos):
    # Ordena para saber quién va detrás de quién en el círculo
    return sorted(vehiculos, key=lambda v: v.angulo)

def calcular_detenciones(vehiculos, radio, distancia_seguridad):
    """
    Devuelve lista paralela indicando si cada vehículo debe detenerse.
    """
    # Si hay 0 o 1 vehículo, no pueden chocar
    if len(vehiculos) < 2:
        return [False] * len(vehiculos)

    ordenados = ordenar_por_angulo(vehiculos)
    n = len(ordenados)

    # Creamos un diccionario para guardar quién debe frenar por ID
    debe_frenar_map = {v.id: False for v in vehiculos}

    for i, vehiculo in enumerate(ordenados):
        siguiente = ordenados[(i + 1) % n]  # El vehículo de enfrente
        
        # Calculamos la distancia real en metros a lo largo del arco
        dist_rad = distancia_angular(vehiculo.angulo, siguiente.angulo)
        dist_metros = dist_rad * radio

        # --- CAMBIO IMPORTANTE ---
        # Antes: solo frenaba si "siguiente.estado == DETENIDO"
        # Ahora: Frena si se rompe la distancia de seguridad, o si el usuario 
        #        frenó manualmente al de adelante.
        
        condicion_distancia = dist_metros < distancia_seguridad
        
        # Si estoy muy cerca -> FRENO (para no chocar)
        # O si el de adelante tiene el freno manual puesto -> FRENO TAMBIÉN
        if condicion_distancia or (condicion_distancia and siguiente.freno_manual):
            debe_frenar_map[vehiculo.id] = True

    # Devolvemos la lista de booleanos en el orden original de la lista 'vehiculos'
    return [debe_frenar_map[v.id] for v in vehiculos]
