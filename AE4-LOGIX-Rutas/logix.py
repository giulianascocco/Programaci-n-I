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


def main():
    modulos, adyacencia = [], []
    opcion = ""
    while opcion != "0":
        print("\n1. Cargar dependencias (RF1)\n2. Grados (RF2)\n0. Salir")
        opcion = input("Opcion: ")
        if opcion == "1":
            modulos, adyacencia = cargar_grafo("dependencias.txt")
            mostrar_matriz(modulos, adyacencia)
        elif opcion == "2" and modulos != []:
            for m in grados(modulos, adyacencia):
                print(m[0], "- salida:", m[1], "- entrada:", m[2])
    print("Fin del programa.")


if __name__ == "__main__":
    main()
