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