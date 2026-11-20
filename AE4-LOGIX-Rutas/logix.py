# LOGIX-Rutas - Analizador de dependencias y navegador de rutas (AE4 - TIFAS 2026)
# Alumnos: Perez Chavez, Ignacio y Scocco Branz, Giuliana Maria - Comision A
#
# Requerimientos que cubre el programa:
#   RF1: cargar los modulos y su matriz de adyacencia desde un archivo
#   RF2: calcular los grados de entrada y salida de cada modulo
#   RF7: calcular la ruta mas rapida entre dos lugares (Dijkstra)
#
# Estructuras de datos usadas:
#   - lista de nombres (nodos): la posicion i de la lista es la fila/columna i de la matriz
#   - matriz (lista de listas): matriz[i][j] es 1 (dependencia) o los minutos de un tramo, 0 si no hay arco

import os

CARPETA = os.path.dirname(os.path.abspath(__file__))   # carpeta donde estan los .txt
INFINITO = 999999                                      # representa "todavia no se llega"


def buscar(nodos, nombre):
    """Busqueda secuencial.
    Recibe: la lista de nodos y el nombre buscado.
    Devuelve: la posicion del nombre en la lista, o -1 si no existe."""
    for i in range(len(nodos)):
        if nodos[i] == nombre:
            return i
    return -1


def cargar_grafo(nombre_archivo, dirigido):
    """Lee un archivo de texto y arma el grafo (RF1).
    Cada linea es 'X;Y' (dependencia, peso 1) o 'X;Y;minutos' (tramo de ruta).
    Recibe: el nombre del archivo y si el grafo es dirigido (True) o no (False).
    Devuelve: la lista de nodos y la matriz de adyacencia (o de pesos)."""
    nodos = []
    arcos = []
    archivo = open(os.path.join(CARPETA, nombre_archivo), "r")
    for linea in archivo:
        partes = linea.strip().split(";")
        peso = "1"                               # sin tercer dato, el arco vale 1
        if len(partes) == 3:
            peso = partes[2]
        # Validacion: hacen falta dos nombres y un peso entero positivo
        if len(partes) < 2 or not peso.isdigit() or int(peso) == 0:
            print("Linea invalida, se ignora:", linea.strip())
        else:
            for nombre in partes[:2]:            # se agregan los nodos nuevos
                if buscar(nodos, nombre) == -1:
                    nodos.append(nombre)
            arcos.append([partes[0], partes[1], int(peso)])
    archivo.close()

    # Matriz de n x n llena de ceros
    matriz = []
    for i in range(len(nodos)):
        matriz.append([0] * len(nodos))
    # Se carga cada arco en su fila (origen) y columna (destino)
    for arco in arcos:
        i = buscar(nodos, arco[0])
        j = buscar(nodos, arco[1])
        matriz[i][j] = arco[2]
        if not dirigido:
            matriz[j][i] = arco[2]      # un tramo se recorre en los dos sentidos (matriz simetrica)
    return nodos, matriz


def mostrar_matriz(nodos, matriz):
    """Muestra la matriz con los nombres de los nodos en filas y columnas."""
    print("    ", *[f"{n:>4}" for n in nodos])
    for i in range(len(nodos)):
        print(f"{nodos[i]:>4} ", *[f"{v:>4}" for v in matriz[i]])


def grados(nodos, matriz):
    """Calcula los grados de cada modulo (RF2).
    Grado de salida = suma de la fila (de cuantos modulos depende).
    Grado de entrada = suma de la columna (cuantos modulos dependen de el).
    Devuelve: lista de [modulo, salida, entrada] ordenada por entrada de mayor a menor."""
    lista = []
    for i in range(len(nodos)):
        salida = 0
        entrada = 0
        for j in range(len(nodos)):
            salida = salida + matriz[i][j]       # suma de la fila i
            entrada = entrada + matriz[j][i]     # suma de la columna i
        lista.append([nodos[i], salida, entrada])
    # Ordenamiento burbuja: compara vecinos y los intercambia si estan desordenados
    for pasada in range(len(lista) - 1):
        for k in range(len(lista) - 1 - pasada):
            if lista[k][2] < lista[k + 1][2]:
                lista[k], lista[k + 1] = lista[k + 1], lista[k]
    return lista


def dijkstra(nodos, matriz, origen, destino):
    """Calcula la ruta mas rapida entre dos lugares (RF7).
    Usa tres listas paralelas: la posicion i corresponde al lugar nodos[i].
    Devuelve: (minutos, camino) o (INFINITO, []) si no hay ruta."""
    n = len(nodos)
    distancia = [INFINITO] * n      # minutos acumulados desde el origen
    anterior = [-1] * n             # desde que lugar se llego (-1 = ninguno)
    definitivo = [False] * n        # True cuando la distancia ya no puede mejorar
    distancia[buscar(nodos, origen)] = 0
    for paso in range(n):
        # 1) Elegir el lugar no definitivo mas cercano
        u = -1
        for i in range(n):
            if not definitivo[i] and (u == -1 or distancia[i] < distancia[u]):
                u = i
        if distancia[u] == INFINITO:             # los que quedan no se pueden alcanzar
            break
        definitivo[u] = True
        # 2) Revisar los vecinos de u: pasando por u se llega antes?
        for v in range(n):
            if matriz[u][v] > 0 and distancia[u] + matriz[u][v] < distancia[v]:
                distancia[v] = distancia[u] + matriz[u][v]
                anterior[v] = u
    # 3) Armar el camino desde el destino hacia atras usando la lista anterior
    d = buscar(nodos, destino)
    camino = []
    actual = d
    while distancia[d] != INFINITO and actual != -1:
        camino.insert(0, nodos[actual])
        actual = anterior[actual]
    return distancia[d], camino


def pedir(nodos, mensaje):
    """Pide un nombre por teclado y lo repite hasta que exista en la lista (validacion)."""
    nombre = input(mensaje).upper()
    while buscar(nodos, nombre) == -1:
        nombre = input("No existe. Opciones " + str(nodos) + ": ").upper()
    return nombre


def main():
    """Programa principal: muestra el menu y llama a las demas funciones."""
    modulos, adyacencia, lugares, pesos = [], [], [], []
    opcion = ""
    while opcion != "0":
        print("\n1. Cargar dependencias (RF1)\n2. Grados (RF2)\n3. Cargar red de rutas\n4. Ruta mas rapida (RF7)\n0. Salir")
        opcion = input("Opcion: ")
        try:
            if opcion == "1":                    # grafo dirigido de dependencias
                modulos, adyacencia = cargar_grafo("dependencias.txt", True)
                mostrar_matriz(modulos, adyacencia)
            elif opcion == "2" and modulos != []:
                for m in grados(modulos, adyacencia):
                    print(m[0], "- salida:", m[1], "- entrada:", m[2])
            elif opcion == "3":                  # grafo no dirigido y ponderado de rutas
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
        except FileNotFoundError:                # el programa no se corta si falta el archivo
            print("No se encontro el archivo.")
    print("Fin del programa.")


if __name__ == "__main__":
    main()
