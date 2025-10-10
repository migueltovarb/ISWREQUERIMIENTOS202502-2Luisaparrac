__author__="Luisa Fernanda Parra Cabrera"
__email__="luisa.parrac@campusucc.edu.co"

import datetime
import csv
import os

PELICULAS= [
    {"codigo": "0877", "titulo": "Barbie", "hora": "3:00 pm", "precio boleto": "$10.000",},
    {"codigo": "4947", "titulo": "El conjuro", "hora": "5:00 pm", "precio boleto": "$10.000", },
    {"codigo": "3091", "titulo": "Perfect Blue",  "hora": "7:00 pm", "precio boleto": "$10.000", },
    {"codigo": "6830", "titulo": "Pinocho",  "hora":"5:00 pm", "precio boleto": "$10.000", }, 
    {"codigo": "9294", "titulo": "La cenicienta",  "hora": "3:00 pm", "precio boleto": "$10.000",},
    {"codigo": "5024", "titulo": "Deadpool",  "hora":"8:00 pm", "precio boleto": "$10.000", },
    {"codigo": "1122", "titulo": "El gato con botas",  "hora": "4:00 pm", "precio boleto": "$10.000",},
    {"codigo": "7788", "titulo": "El hombre araña",  "hora": "6:00 pm", "precio boleto": "$10.000",},
    {"codigo": "5566", "titulo": "Titanic",  "hora": "7:00 pm", "precio boleto": "$10.000",},
]

FUNCIONES = {}

LOG_FILE = "registro_" \
"boletos_diario.txt"

def registrar_funcion():
    print("\n--- 👤 REGISTRO DE NUEVA FUNCION ---")
    id_funcion = input("Ingrese el codigo de la pelicula: ").strip()

    if id_funcion in FUNCIONES:
        print(f"⚠️ El codigo {id_funcion} ya está registrado. Intente con otro.")
        return

    nombre = input("Ingrese el Nombre: ").strip()
    hora = input("Ingrese la hora de la función: ").strip()
    precio_boleto = input("Ingrese el precio del boleto: ").strip()
    
    FUNCIONES[id_funcion] = {
        'nombre': nombre,
        'hora': hora,
        'precio_boleto': precio_boleto, 
        'funciones_vendidas': 0  
    }
    print(f"\n✅ Funcion {nombre} ({hora.capitalize()}) registrado con éxito.")
    print(f"Su ID de funcion es: {id_funcion}")

# ---

def listar_funciones():
    """
    Muestra la lista de todas las películas disponibles en el cine.
    """
    print("\n=== 🎬 CARTELERA MOVIETIME 🎬 ===")
    print("-" * 75)
    print(f"{'CÓDIGO':<8} | {'TÍTULO':<20} | {'HORA':<10} | {'PRECIO':<10}")
    print("-" * 75)
    
    for pelicula in PELICULAS:
        print(f"{pelicula['codigo']:<8} | {pelicula['titulo']:<20} | {pelicula['hora']:<10} | {pelicula['precio boleto']:<10}")
    
    print("-" * 75)
    print(f"Total de películas disponibles: {len(PELICULAS)}")
    return PELICULAS

def vender_boletos():
    print("\n=== 🎟️ VENTA DE BOLETOS 🎟️ ===")
    
    listar_funciones()
    
    codigo = input("\nIngrese el código de la película: ").strip()
 
    pelicula = None
    for p in PELICULAS:
        if p['codigo'] == codigo:
            pelicula = p
            break
    
    if not pelicula:
        print("❌ Error: Código de película no válido.")
        return
    
    try:
        cantidad = int(input("Ingrese la cantidad de boletos: "))
        if cantidad <= 0:
            print("❌ Error: La cantidad debe ser mayor a 0.")
            return
    except ValueError:
        print("❌ Error: Por favor ingrese un número válido.")
        return

    precio = float(pelicula['precio boleto'].replace('$', '').replace('.', ''))
    total = precio * cantidad
    
    # Mostrar resumen de la compra
    print("\n=== RESUMEN DE LA COMPRA ===")
    print(f"Película: {pelicula['titulo']}")
    print(f"Hora: {pelicula['hora']}")
    print(f"Cantidad de boletos: {cantidad}")
    print(f"Precio por boleto: {pelicula['precio boleto']}")
    print(f"Total a pagar: ${total:,.0f}")
    
    # Confirmar compra
    confirmacion = input("\n¿Desea confirmar la compra? (s/n): ").lower()
    if confirmacion != 's':
        print("Compra cancelada.")
        return
    
    # Registrar la venta en el archivo de registro
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, 'a', newline='') as file:
            file.write(f"{fecha_actual},{pelicula['codigo']},{pelicula['titulo']},{cantidad},{total}\n")
        print("\n✅ ¡Venta realizada con éxito!")
        print("Se ha guardado el registro de la venta.")
    except Exception as e:
        print(f"\n❌ Error al guardar el registro de la venta: {e}")


# --- 3. MENÚ PRINCIPAL ---

def main():
    """Función principal para el menú de consola."""
    while True:
        print("\n==============================================")
        print("  🟢 BIENVENIDO a MovieTime 🟢")
        print("==============================================")
        print("1. 👤 Registrar Nueva Función") 
        print("2. 📖 Listar Funciones Disponibles")
        print("3. 🎟️ Vender Boletos")
        print("4. 💾 Ver Registro Diario")
        print("5. 🚪 Salir")
        print("----------------------------------------------")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            registrar_funcion()
        elif opcion == '2':
            listar_funciones()
        elif opcion == '3':
            vender_boletos()
        elif opcion == '4':
            print(f"\n--- 💾 Contenido del archivo de Registro Diario ({LOG_FILE}) ---")
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r') as f:
                    print(f.read())
            else:
                print("El archivo de registro diario aún no existe.")
            print("-" * 50)
        elif opcion == '5':
            print("¡Gracias por usar MovieTime! Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()