# LOGIX-Rutas - Analizador de dependencias y navegador de rutas (AE4 - TIFAS 2026)

import os

CARPETA = os.path.dirname(os.path.abspath(__file__))


def buscar(nodos, nombre):
    """Busqueda secuencial: posicion del nodo o -1 si no existe."""
    for i in range(len(nodos)):
        if nodos[i] == nombre:
            return i
    return -1


def cargar_grafo(nombre_archivo):
    """Lee lineas 'X;Y' (X depende de Y) y arma la matriz de adyacencia."""
    nodos = []
    arcos = []
    archivo = open(os.path.join(CARPETA, nombre_archivo), "r")
    for linea in archivo:
        partes = linea.strip().split(";")
        for nombre in partes:
            if buscar(nodos, nombre) == -1:
                nodos.append(nombre)
        arcos.append([partes[0], partes[1]])
    archivo.close()

    matriz = []
    for i in range(len(nodos)):
        matriz.append([0] * len(nodos))
    for arco in arcos:
        matriz[buscar(nodos, arco[0])][buscar(nodos, arco[1])] = 1
    return nodos, matriz


def mostrar_matriz(nodos, matriz):
    print("    ", *[f"{n:>4}" for n in nodos])
    for i in range(len(nodos)):
        print(f"{nodos[i]:>4} ", *[f"{v:>4}" for v in matriz[i]])


def main():
    modulos, adyacencia = [], []
    opcion = ""
    while opcion != "0":
        print("\n1. Cargar dependencias (RF1)\n0. Salir")
        opcion = input("Opcion: ")
        if opcion == "1":
            modulos, adyacencia = cargar_grafo("dependencias.txt")
            mostrar_matriz(modulos, adyacencia)
    print("Fin del programa.")


if __name__ == "__main__":
    main()
