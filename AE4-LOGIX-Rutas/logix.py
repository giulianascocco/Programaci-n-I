# LOGIX-Rutas - Analizador de dependencias y navegador de rutas (AE4 - TIFAS 2026)

import os

CARPETA = os.path.dirname(os.path.abspath(__file__))
INFINITO = 999999


def buscar(nodos, nombre):
    """Busqueda secuencial: posicion del nodo o -1 si no existe."""
    for i in range(len(nodos)):
        if nodos[i] == nombre:
            return i
    return -1


def cargar_grafo(nombre_archivo, dirigido):
    """Lee lineas 'X;Y' (dependencias) o 'X;Y;minutos' (tramos) y arma la matriz."""
    nodos = []
    arcos = []
    archivo = open(os.path.join(CARPETA, nombre_archivo), "r")
    for linea in archivo:
        partes = linea.strip().split(";")
        peso = "1"
        if len(partes) == 3:
            peso = partes[2]
        if len(partes) < 2 or not peso.isdigit() or int(peso) == 0:
            print("Linea invalida, se ignora:", linea.strip())
        else:
            for nombre in partes[:2]:
                if buscar(nodos, nombre) == -1:
                    nodos.append(nombre)
            arcos.append([partes[0], partes[1], int(peso)])
    archivo.close()

    matriz = []
    for i in range(len(nodos)):
        matriz.append([0] * len(nodos))
    for arco in arcos:
        i = buscar(nodos, arco[0])
        j = buscar(nodos, arco[1])
        matriz[i][j] = arco[2]
        if not dirigido:
            matriz[j][i] = arco[2]      # un tramo se recorre en los dos sentidos
    return nodos, matriz


def mostrar_matriz(nodos, matriz):
    print("    ", *[f"{n:>4}" for n in nodos])
    for i in range(len(nodos)):
        print(f"{nodos[i]:>4} ", *[f"{v:>4}" for v in matriz[i]])


def grados(nodos, matriz):
    """Devuelve [modulo, salida, entrada] ordenado por grado de entrada (burbuja)."""
    lista = []
    for i in range(len(nodos)):
        salida = 0
        entrada = 0
        for j in range(len(nodos)):
            salida = salida + matriz[i][j]       # suma de la fila i
            entrada = entrada + matriz[j][i]     # suma de la columna i
        lista.append([nodos[i], salida, entrada])
    for pasada in range(len(lista) - 1):
        for k in range(len(lista) - 1 - pasada):
            if lista[k][2] < lista[k + 1][2]:
                lista[k], lista[k + 1] = lista[k + 1], lista[k]
    return lista


def dijkstra(nodos, matriz, origen, destino):
    """Devuelve (minutos, camino) de la ruta mas rapida, o (INFINITO, []) si no hay."""
    n = len(nodos)
    distancia = [INFINITO] * n
    anterior = [-1] * n
    definitivo = [False] * n
    distancia[buscar(nodos, origen)] = 0
    for paso in range(n):
        u = -1                                   # lugar no definitivo mas cercano
        for i in range(n):
            if not definitivo[i] and (u == -1 or distancia[i] < distancia[u]):
                u = i
        if distancia[u] == INFINITO:
            break
        definitivo[u] = True
        for v in range(n):                       # pasando por u se llega antes?
            if matriz[u][v] > 0 and distancia[u] + matriz[u][v] < distancia[v]:
                distancia[v] = distancia[u] + matriz[u][v]
                anterior[v] = u
    d = buscar(nodos, destino)
    camino = []
    actual = d
    while distancia[d] != INFINITO and actual != -1:   # se arma desde el destino hacia atras
        camino.insert(0, nodos[actual])
        actual = anterior[actual]
    return distancia[d], camino


def pedir(nodos, mensaje):
    nombre = input(mensaje).upper()
    while buscar(nodos, nombre) == -1:
        nombre = input("No existe. Opciones " + str(nodos) + ": ").upper()
    return nombre


def main():
    modulos, adyacencia, lugares, pesos = [], [], [], []
    opcion = ""
    while opcion != "0":
        print("\n1. Cargar dependencias (RF1)\n2. Grados (RF2)\n3. Cargar red de rutas\n4. Ruta mas rapida (RF7)\n0. Salir")
        opcion = input("Opcion: ")
        try:
            if opcion == "1":
                modulos, adyacencia = cargar_grafo("dependencias.txt", True)
                mostrar_matriz(modulos, adyacencia)
            elif opcion == "2" and modulos != []:
                for m in grados(modulos, adyacencia):
                    print(m[0], "- salida:", m[1], "- entrada:", m[2])
            elif opcion == "3":
                archivo = input("Archivo [red_distribucion.txt]: ") or "red_distribucion.txt"
                lugares, pesos = cargar_grafo(archivo, False)
                mostrar_matriz(lugares, pesos)
            elif opcion == "4" and lugares != []:
                minutos, camino = dijkstra(lugares, pesos, pedir(lugares, "Origen: "), pedir(lugares, "Destino: "))
                if camino == []:
                    print("No hay ruta entre esos lugares.")
                else:
                    print(" - ".join(camino), "=", minutos, "min")
            elif opcion != "0":
                print("Opcion invalida o falta cargar los datos (opcion 1 o 3).")
        except FileNotFoundError:
            print("No se encontro el archivo.")
    print("Fin del programa.")


if __name__ == "__main__":
    main()
