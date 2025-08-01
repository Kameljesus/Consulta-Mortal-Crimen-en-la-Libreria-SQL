numero_posible = input('ingrese un numero en letra')

opciones = {
    'Uno': 1,
    'Dos': 2,
    'Tres': 3,
}

if numero_posible in opciones:
    print(f"El número es: {opciones[numero_posible]}")
else:
    print("❌ Entrada no válida.")
