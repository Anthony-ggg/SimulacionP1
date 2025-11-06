# main.py
from cajero import Cajero, generar_cajas
from cajero_express import CajeroExpress
from simulador import simular_todas
from SimuladorVisual import simular_visual


def main():
    print("=== SIMULADOR DE FILAS EN SUPERMERCADO ===\n")

    #Configuracion automatica
    num_cajas = int(input("Ingresa numero de cajas normales:"))
    cajas = generar_cajas(num_cajas,Cajero,CajeroExpress)

    

    print("Configuración inicial:\n")
    for caja in cajas:
        print(f" - {caja.nombre}| Clientes: {caja.clientes} | Artículos por cliente: {caja.articulos_por_cliente}")

    print("\n--- CÁLCULO DETALLADO DE TIEMPOS ---")

    tiempos = {}

    for caja in cajas:
        print(f"\n--- {caja.nombre}")
        total_caja = 0

        for idx, articulos in enumerate(caja.articulos_por_cliente, start=1):
            tiempo_total, tiempos_articulos, tiempo_cobro = caja.calcular_tiempo_cliente(articulos)

            print(f" Cliente {idx}: {articulos} artículos")
            print(f" Tiempo de scaneo por artículo: {tiempos_articulos}")
            print(f" Escaneo total: {sum(tiempos_articulos)} s")
            print(f" tiempo de Cobro: {tiempo_cobro} s")
            print(f" Tiempo total de atencion al cliente: {tiempo_total} s\n")

            total_caja += tiempo_total

        tiempos[caja.nombre] = total_caja
        print(f"***> TOTAL {caja.nombre}: {total_caja} s ({total_caja/60:.2f} min)")

    # Determinar la caja más rápida
    mejor_caja = min(tiempos, key=tiempos.get)
    print(f"\n✅ La mejor opción para salir más rápido es: {mejor_caja}")

    # Ejecutar la simulación visual inmediatamente (sin preguntar)
    simular_visual(cajas)

    


    
if __name__ == "__main__":
    main()


    