# cajero.py
import random
class Cajero:
    def __init__(self, nombre, articulos_por_cliente):
        """
        nombre: str -> nombre de la caja
        tiempo_escaneo: float -> segundos por artículo
        articulos_por_cliente: list[int] -> lista con los artículos de cada cliente
        """
        self.nombre = nombre
        self.articulos_por_cliente = articulos_por_cliente
        self.clientes = len(articulos_por_cliente)

    def calcular_tiempo_cliente(self, articulos):
    #Calcualr cada tiempo de cliente
        
        # Guardar tiempo por cada artículo
        tiempos_articulos = [random.randint(5, 9) for _ in range(articulos)] # se demora en escanear entre 5-9 s
        tiempo_escaneo_total = sum(tiempos_articulos)

        tiempo_cobro = random.randint(15, 30)  # Tiempo demora de cobro variable entre 15 y 30 segundos

        #tiempo total de atencion al cliente
        tiempo_total = tiempo_escaneo_total + tiempo_cobro
        return tiempo_total, tiempos_articulos, tiempo_cobro

    def calcular_tiempo_total(self):
        # da tiempo total de todos los clientes en la fila
        total = 0
        for articulos in self.articulos_por_cliente:
            tiempo_total, _,_ = self.calcular_tiempo_cliente(articulos)
            total += tiempo_total
        return total

    def __str__(self):
        return f"{self.nombre}  - Clientes: {self.clientes}"
    

#GENERAR CAJAS 

def generar_clientes_aleatorios(num_clientes, max_articulos): 
        #Genera una lista con un número aleatorio de artículos por cliente.
    return [random.randint(1, max_articulos) for _ in range(num_clientes)] 
    
    
def generar_cajas(num_cajas, CajeroClass, ExpressClass):
        #Crea cajas normales y una express automáticamente.
     cajas = []
        # Cajas normales
     for i in range(1, num_cajas + 1):
         num_clientes = random.randint(1, 3)
         clientes = generar_clientes_aleatorios(num_clientes, max_articulos= 20)
         cajas.append(CajeroClass(f"Caja {i}", clientes))

    # Caja express
     num_clientes_express = random.randint(3, 6)
     clientes_express = generar_clientes_aleatorios(num_clientes_express,max_articulos=10)
     cajas.append(ExpressClass("Caja Express", clientes_express))

     return cajas
