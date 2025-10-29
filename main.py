# main.py
from cajero import Cajero
from cajero_express import CajeroExpress

def main():
    print("=== SIMULADOR DE FILAS EN SUPERMERCADO ===\n")

    # Definimos las cajas con sus clientes y artículos
    cajas = [
        Cajero("Caja 1",  articulos_por_cliente=[12, 1]),
        CajeroExpress("Caja Express", articulos_por_cliente=[5, 8]),
    ]

    print("Configuración inicial:\n")
    for c in cajas:
        print(f" - {c} | Artículos por cliente: {c.articulos_por_cliente}")

    print("\n--- CÁLCULO DETALLADO DE TIEMPOS ---")

    tiempos = {}

    for caja in cajas:
        print(f"\n--- {caja.nombre}")
        total_caja = 0

        for idx, articulos in enumerate(caja.articulos_por_cliente, start=1):
            tiempo_total, tiempos_articulos, tiempo_cobro = caja.calcular_tiempo_cliente(articulos)

            print(f" Cliente {idx}: {articulos} artículos")
            print(f" Tiempo de scaneo por artículo: {tiempos_articulos}")
            print(f" Escaneo total: {sum(tiempos_articulos)}s")
            print(f" Cobro: {tiempo_cobro}s")
            print(f" Tiempo total cliente: {tiempo_total}s\n")

            total_caja += tiempo_total

        tiempos[caja.nombre] = total_caja
        print(f"➡ TOTAL {caja.nombre}: {total_caja}s ({total_caja/60:.2f} min)")

    # Determinar la caja más rápida
    mejor_caja = min(tiempos, key=tiempos.get)
    print(f"\n✅ La mejor opción para salir más rápido es: {mejor_caja}")

    
if __name__ == "__main__":
    main()

# cuanto tiene que esperar el 
