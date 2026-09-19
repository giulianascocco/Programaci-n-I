alumnos = [
    {"nombre": "Juan", "notas": [7, 8, 9, 6], "asistencia": 90},
    {"nombre": "Maria", "notas": [5, 6, 4, 7], "asistencia": 60},
    {"nombre": "Pedro", "notas": [1, 9, 4, 7], "asistencia": 95},
    {"nombre": "Ana", "notas": [6, 5, 7, 8], "asistencia": 85}
]

def calcular_promedio(notas):
    suma_total = 0
    cantidad_notas = 0
    for nota in notas:
        suma_total = suma_total + nota
        cantidad_notas = cantidad_notas + 1
    return suma_total / cantidad_notas

def es_regular(alumno):
    promedio = calcular_promedio(alumno["notas"])
    return promedio >= 6 and alumno["asistencia"] >= 75

def verificar_estado_alumnos(lista_alumnos):
    for alumno in lista_alumnos:
        promedio = calcular_promedio(alumno["notas"])
        if es_regular(alumno):
            estado = "REGULAR"
        else:
            estado = "NO REGULAR (Libre)"
        print(f"Alumno: {alumno['nombre']} | Promedio: {promedio:.2f} | Asistencia: {alumno['asistencia']}% -> Estado: {estado}")

verificar_estado_alumnos(alumnos)