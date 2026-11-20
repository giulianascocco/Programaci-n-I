# Pruebas de LOGIX (ejecutar con: python pruebas.py)
from logix import *

def prueba(nombre, esperado, obtenido):
    print("OK   " if esperado == obtenido else "FALLA", nombre, "" if esperado == obtenido else obtenido)

modulos, A = cargar_grafo("dependencias.txt", True)
prueba("P1 Carga de los 9 modulos (Tabla 2)", 9, len(modulos))
prueba("P2 PED depende de CLI, INV y ASG", 1, A[0][buscar(modulos, "CLI")] * A[0][buscar(modulos, "INV")] * A[0][buscar(modulos, "ASG")])
g = grados(modulos, A)
prueba("P3 Modulo mas critico: INV, entrada 4", ["INV", 1, 4], g[0])
prueba("P4 Total de dependencias = 14", 14, sum(m[1] for m in g))
prueba("P5 Caso limite: CLI sin dependencias", 0, g[buscar([m[0] for m in g], "CLI")][1])

lugares, W = cargar_grafo("red_distribucion.txt", False)
prueba("P6 Ruta mas rapida D a Z3", (16, ["D", "H2", "Z2", "Z3"]), dijkstra(lugares, W, "D", "Z3"))
prueba("P7 Caso limite: origen = destino", (0, ["D"]), dijkstra(lugares, W, "D", "D"))
lugares2, W2 = cargar_grafo("red_con_dron.txt", False)
prueba("P8 Con corredor de dron D-Z3", (14, ["D", "Z3"]), dijkstra(lugares2, W2, "D", "Z3"))
lugares3, W3 = cargar_grafo("red_desconectada.txt", False)
prueba("P9 Caso limite: zona sin conexion", (INFINITO, []), dijkstra(lugares3, W3, "D", "Z4"))
lugares4, W4 = cargar_grafo("red_invalida.txt", False)
prueba("P10 Caso limite: minutos negativos", ["D", "H1"], lugares4)
