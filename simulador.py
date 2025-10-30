# simulador.py
import time
import os
import random


# UTILIDADES BÁSICAS

def limpiar():
    """Limpia la consola """
    os.system("cls")

def barra_progreso(actual, total, largo=20):
    """Devuelve una barra de progreso visual tipo [█████-----]."""
    completado = int((actual / total) * largo)
    return "█" * completado + "-" * (largo - completado)

# SIMULACIÓN DE TODAS LAS CAJAS EN PARALELO

def simular_todas(cajas):
    """
    Simula todas las cajas intercaladas (sin hilos), mostrando:
      - Escaneo de artículos
      - Pago
      - Cliente atendido
    Al finalizar:
      - Total de clientes atendidos
      - Tiempo total estimado
      - Caja más rápida
    """
    limpiar()
    print(" SIMULACIÓN DE TODAS LAS CAJAS \n")
    time.sleep(1)

    # Estado inicial de cada caja
    estados = [{
        "caja": caja,                         # Objeto caja actual
        "cliente": 0,                         # Índice del cliente actual
        "articulo": 1,                        # Artículo en curso
        "articulos": caja.articulos_por_cliente[0],  # Total de artículos
        "fase": "escaneo",                    # Fase inicial
        "contador": 0                         # Tiempo de pago restante
    } for caja in cajas if caja.articulos_por_cliente]

    # Diccionario para guardar el tiempo total por caja
    tiempos_totales = {caja.nombre: 0 for caja in cajas}

    # Bucle principal — continúa mientras existan cajas activas
    while estados:
        limpiar()
        print(" ESTADO ACTUAL DEL SUPERMERCADO\n")

        nuevos_estados = []

        for e in estados:
            caja = e["caja"]
            cliente = e["cliente"] + 1
            articulos = e["articulos"]
            art_actual = e["articulo"]

            # ====== FASE 1: Escaneo ======
            if e["fase"] == "escaneo":
                total_clientes = len(caja.articulos_por_cliente)
                clientes_atendidos = e["cliente"]   # Cuántos ya se atendieron
                cliente_actual = cliente            # Cuál se está atendiendo ahora

                print(
                    f"⏳ {caja.nombre:<14} "
                    f"Cliente {cliente_actual}/{total_clientes} "
                    f"({articulos} art.) 🔄 [{barra_progreso(art_actual, articulos)}] {art_actual}/{articulos}"
                )
                
                # Avance interno del cliente
                e["articulo"] += 1
                tiempos_totales[caja.nombre] += 1  # tiempo simulado acumulado

                # Si termina de escanear todos los artículos → pasa a pago
                if e["articulo"] > articulos:
                    e["fase"] = "pago"
                    e["contador"] = random.randint(2, 4)
                
                nuevos_estados.append(e)

            # ====== FASE 2: Pago ======
            elif e["fase"] == "pago":
                print(f"🤑 {caja.nombre:<14} Cliente {cliente:<2} pagando... ({e['contador']}s)")
                e["contador"] -= 1
                tiempos_totales[caja.nombre] += 1  # Tiempo de pago

                if e["contador"] > 0:
                    nuevos_estados.append(e)
                else:
                    e["fase"] = "finalizado"
                    nuevos_estados.append(e)

            # ====== FASE 3: Cliente atendido ======
            elif e["fase"] == "finalizado":
                print(f"🫶 {caja.nombre:<14} Cliente {cliente:<2} atendido ✅")

                # Pasar al siguiente cliente
                e["cliente"] += 1
                if e["cliente"] < len(caja.articulos_por_cliente):
                    e.update({
                        "articulo": 1,
                        "articulos": caja.articulos_por_cliente[e["cliente"]],
                        "fase": "escaneo",
                    })
                    nuevos_estados.append(e)
                # Si no quedan más clientes → caja finaliza

        
        # Actualiza estados y ritmo de simulación
        estados = nuevos_estados
        time.sleep(1.25)


   
    # RESUMEN FINAL DE RESULTADOS

    # Calculamos totales simulados
    total_clientes = sum(len(caja.articulos_por_cliente) for caja in cajas)
    mejor_caja = min(tiempos_totales, key=tiempos_totales.get)

    
    limpiar()
    print("  RESUMEN   FINAL")
    print("═" * 50 + "\n")

    # Datos globales
    print(f" Total de clientes atendidos: {total_clientes}")

    # Resultados por caja
    print("  RESULTADOS POR CAJA:\n")
    for caja in cajas:
        nombre = caja.nombre
        tiempo_total = tiempos_totales[nombre]
        clientes_caja = len(caja.articulos_por_cliente)
        print(f"🖥️-{nombre:<14} → {clientes_caja:>2} cliente(s) | {tiempo_total:>6.2f} s totales ")

    # Caja más rápida
    print("\n Caja más eficiente:  {0}  ({1:.2f} s)".format(mejor_caja, tiempos_totales[mejor_caja]))
    time.sleep(1)