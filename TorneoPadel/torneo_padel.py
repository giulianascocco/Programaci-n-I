cantidadJugadores = int(input("¿Cuantos jugadores van a participar en el torneo? "))
nombresJugadores = [] 
categoriasJugadores = []

for i in range(cantidadJugadores): 
    print(f"\nJugador #{i+1}:")
    nombre = input("Ingrese el nombre del jugador: ")
    categoria = input("Ingrese la categoria del jugador: ")
    nombresJugadores.append(nombre)
    categoriasJugadores.append(categoria) 

print("\n Jugadores inscriptos: ")
for i in range (len(nombresJugadores)):
    print(f"- {nombresJugadores[i]} (Categoria: {categoriasJugadores[i]})")

    if cantidadJugadores % 2 != 0:
        print("Error: El torneo de pádel requiere un número par de jugadores para formar parejas.")
else:
    cantidadParejas = cantidadJugadores // 2

nombresParejas = []
parejasIntegrante1 = []
parejasIntegrante2 = []

print(f"\nArmado de Parejas ({cantidadParejas} parejas en total)")

for i in range(cantidadParejas):
    print(f"\nPareja #{i + 1}:")
    nombreP = input("Ingrese el nombre de la pareja: ")
    j1 = input("Ingrese el nombre del primer jugador: ")
    j2 = input("Ingrese el nombre del segundo jugador: ")
    
    # Agregamos los valores a las listas
    nombresParejas.append(nombreP)
    parejasIntegrante1.append(j1)
    parejasIntegrante2.append(j2)

    print("\n PAREJAS CONFIRMADAS EN EL TORNEO ")
for i in range(len(nombresParejas)):
    print(f"Pareja '{nombresParejas[i]}': {parejasIntegrante1[i]} y {parejasIntegrante2[i]}")