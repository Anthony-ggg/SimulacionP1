# main.py
from cajero import Cajero
from cajero_express import CajeroExpress

def main():
    print("=== SIMULADOR DE FILAS EN SUPERMERCADO ===\n")

    # Definimos las cajas con sus clientes y artículos
    cajas = [
        Cajero("Caja 1", tiempo_escaneo=5, articulos_por_cliente=[12, 25, 7, 6]),
        Cajero("Caja 2", tiempo_escaneo=5, articulos_por_cliente=[30, 40, 18]),
        Cajero("Caja 3", tiempo_escaneo=9, articulos_por_cliente=[20, 50, 45, 10, 25]),
        CajeroExpress("Caja Express", tiempo_escaneo=5, articulos_por_cliente=[5, 8, 12, 3, 6, 15,11,11,11,11]),
    ]

    print("Configuración inicial:\n")
    for c in cajas:
        print(f" - {c} | Artículos por cliente: {c.articulos_por_cliente}")

    print("\n--- CÁLCULO DE TIEMPOS ---")
    tiempos = {}
    for caja in cajas:
        total = caja.calcular_tiempo_total()
        tiempos[caja.nombre]  = total
        print(f"{caja.nombre} -> Tiempo total: {total:.2f} segundos ({total/60:.2f} min)")
 
    # Determinar la caja más rápida
    mejor_caja = min(tiempos, key=tiempos.get)
    print(f"\n✅ La mejor opción para salir más rápido es: {mejor_caja}")

if __name__ == "__main__":
    main()
