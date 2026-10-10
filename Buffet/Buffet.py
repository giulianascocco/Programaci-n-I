CODIGOS = [101, 102, 103, 104, 105, 106]
NOMBRES = [
    "Café con leche",
    "Medialuna",
    "Sándwich de miga",
    "Agua mineral 500ml",
    "Empanada",
    "Chipá (100g)"
]
PRECIOS = [1500.0, 700.0, 1800.0, 1000.0, 1200.0, 1300.0]
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

NOMBRE_ARCHIVO = "ventas_semana.txt"

def inicializar_matriz():
    """Crea una matriz de 5x6 llena de ceros (5 días hábiles x 6 productos)."""
    matriz = []
    for f in range(5):
        fila = [0] * 6
        matriz.append(fila)
    return matriz

def cargar_desde_archivo(nombre_archivo):
    """
    Lee el archivo secuencial de texto para reconstruir la matriz en la memoria RAM.
    Maneja la excepción si el archivo no existe para iniciar con una matriz limpia.
    """
    matriz = inicializar_matriz()
    try:
        archivo = open(nombre_archivo, "r")
        f = 0
        for linea in archivo:
            linea_limpia = linea.strip()
            if linea_limpia and f < 5:
                valores = linea_limpia.split(",")
                for c in range(min(len(valores), 6)):
                    matriz[f][c] = int(valores[c])
                f += 1
        archivo.close()
        print(f"[SISTEMA] Datos cargados correctamente desde '{nombre_archivo}'.")
    except FileNotFoundError:
        print(f"[ALERTA] No se encontró '{nombre_archivo}'. Se inicia matriz vacía.")
    return matriz

def guardar_en_archivo(nombre_archivo, matriz):
    """Guarda el estado actual de la matriz de ventas en el archivo secundario."""
    archivo = open(nombre_archivo, "w")
    for fila in matriz:
        linea = ",".join(map(str, fila)) + "\n"
        archivo.write(linea)
    archivo.close()
    print(f"[SISTEMA] Datos guardados exitosamente en '{nombre_archivo}'.")

def buscar_posicion_codigo(codigo):
    """Busca un código en el vector paralelo CODIGOS y devuelve su índice."""
    for i in range(len(CODIGOS)):
        if CODIGOS[i] == codigo:
            return i
    return -1

def registrar_venta_diaria(matriz):
    """Carga y acumula unidades vendidas en la celda [día][producto] de la matriz."""
    print("\n--- REGISTRO DE VENTA DIARIA ---")
    print("Seleccione el día de la semana:")
    for i in range(len(DIAS)):
        print(f"  {i}. {DIAS[i]}")
    
    try:
        dia_idx = int(input("Ingrese el número correspondiente al día (0-4): "))
        if dia_idx < 0 or dia_idx > 4:
            print("[ERROR] Día inválido. Debe seleccionar entre 0 y 4.")
            return

        cod = int(input("Ingrese el código del producto (101 a 106): "))
        prod_idx = buscar_posicion_codigo(cod)
        if prod_idx == -1:
            print("[ERROR] El código ingresado no existe en el catálogo.")
            return

        cant = int(input(f"Ingrese la cantidad vendida de '{NOMBRES[prod_idx]}': "))
        if cant <= 0:
            print("[ERROR] La cantidad debe ser mayor a cero.")
            return

        # Acumulamos las unidades vendidas en la matriz bidimensional
        matriz[dia_idx][prod_idx] += cant
        print(f"[ÉXITO] Se agregaron {cant} unidades a '{NOMBRES[prod_idx]}' para el día {DIAS[dia_idx]}.")

    except ValueError:
        print("[ERROR] Debe ingresar únicamente valores numéricos enteros.")

def mostrar_reportes_semanales(matriz):
    """Procesa la matriz de ventas y calcula las métricas requeridas."""
    print("\n=======================================================")
    print("        INFORME CONSOLIDADO DE VENTAS SEMANALES       ")
    print("=======================================================")

    # 1. Total de unidades vendidas por producto (suma por columnas)
    totales_producto = [0] * 6
    for c in range(6):
        suma_columna = 0
        for f in range(5):
            suma_columna += matriz[f][c]
        totales_producto[c] = suma_columna

    print("\n1. Unidades vendidas por producto:")
    for c in range(6):
        print(f"   - {NOMBRES[c]} (Cód: {CODIGOS[c]}): {totales_producto[c]} unidades")

    # 2. Recaudación diaria y semanal (suma por filas * precio)
    recaudacion_diaria = [0.0] * 5
    total_semanal = 0.0

    print("\n2. Recaudación diaria:")
    for f in range(5):
        monto_dia = 0.0
        for c in range(6):
            monto_dia += matriz[f][c] * PRECIOS[c]
        recaudacion_diaria[f] = monto_dia
        total_semanal += monto_dia
        print(f"   - {DIAS[f]}: ${monto_dia:.2f}")

    print(f"\n3. Recaudación TOTAL acumulada en la semana: ${total_semanal:.2f}")

    # 4. Producto más vendido y Día de mayor ingreso
    max_cant_prod = max(totales_producto)
    max_prod_idx = totales_producto.index(max_cant_prod)

    max_monto_dia = max(recaudacion_diaria)
    max_dia_idx = recaudacion_diaria.index(max_monto_dia)

    print(f"\n4. Producto más vendido: {NOMBRES[max_prod_idx]} ({max_cant_prod} unidades).")
    print(f"5. Día de mayor recaudación: {DIAS[max_dia_idx]} (${max_monto_dia:.2f}).")

    # 6. Productos sin ventas registradas
    print("\n6. Productos sin ventas en la semana:")
    sin_ventas = False
    for c in range(6):
        if totales_producto[c] == 0:
            print(f"   - {NOMBRES[c]} (Cód: {CODIGOS[c]})")
            sin_ventas = True
    if not sin_ventas:
        print("   (Todos los productos registraron al menos una venta).")

def menu_principal():
    """Flujo principal y menú de opciones."""
    matriz_ventas = cargar_desde_archivo(NOMBRE_ARCHIVO)

    opcion = ""
    while opcion != "3":
        print("     BUFFET FACULTAD - GESTIÓN DE VENTAS  ")
        print("1. Registrar Venta Diaria")
        print("2. Ver Reportes de la Semana")
        print("3. Guardar Cambios y Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_venta_diaria(matriz_ventas)
        elif opcion == "2":
            mostrar_reportes_semanales(matriz_ventas)
        elif opcion == "3":
            guardar_en_archivo(NOMBRE_ARCHIVO, matriz_ventas)
            print("Hasta luego")
        else:
            print("[ERROR] Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()