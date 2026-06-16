"""
Archivo principal que ejecuta el Menú Principal.
"""

from modelos import clsUsuarios, clsItem
from gestor_archivos import guardar_usuario, cargar_usuarios, guardar_item, cargar_inventario

def mostrar_menu():
    """Dibuja la interfaz visual amigable en la consola"""
    print("\n=============================================")
    print("      SISTEMA DE GESTIÓN PRESTAFÁCIL         ")
    print("=============================================")
    print("1. Registrar Amigo / Usuario")
    print("2. Registrar Ítem (Objeto al Inventario)")
    print("3. Registrar Préstamo")
    print("4. Registrar y Certificar Devolución")
    print("5. Generar Venta (>30 días)")
    print("6. Consultar Estado General de Préstamos")
    print("7. Módulo Administrador")
    print("8. Salir del Programa")
    print("=============================================")

def ejecutar_registrar_usuario():
    """Captura los datos del usuario y maneja los errores de validación"""
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    try:
        nombre = input("Ingrese el nombre: ")
        apellido = input("Ingrese el apellido: ")
        documento = input("Ingrese el documento (solo números): ")
        correo = input("Ingrese el correo electrónico: ")
        
        print("Tiempos de préstamo permitidos: 5, 10, 15 o 30 días.")
        tiempo = int(input("Seleccione el tiempo de préstamo (en días): "))
        
        nuevo_usuario = clsUsuarios(nombre, apellido, documento, correo, tiempo)
        
        guardar_usuario(nuevo_usuario)
        print("\n¡Éxito! Usuario registrado y guardado correctamente.")
        
    except ValueError as e:
        print(f"\n[ERROR DE VALIDACIÓN] -> {e}")
        print("Por favor, intente el registro nuevamente con datos válidos.")

def ejecutar_registrar_item():
    """Captura los datos de un ítem y le calcula el estado difuso"""
    print("\n--- REGISTRO DE NUEVO ÍTEM ---")
    try:
        nombre = input("Nombre del artículo: ")
        
        print("\nCategorías disponibles:")
        print("1. Videojuegos\n2. Libros\n3. Música y video\n4. Herramientas\n5. Dinero\n6. Misceláneo y varios")
        opc_cat = input("Seleccione el número de la categoría: ")
        
        mapa_categorias = {
            "1": "Videojuegos", "2": "Libros", "3": "Música y video",
            "4": "Herramientas", "5": "Dinero", "6": "Misceláneo y varios"
        }
        categoria = mapa_categorias.get(opc_cat, "Invalida")

        precio = float(input("Precio de compra (costo de adquisición): "))
        porcentaje_calidad = float(input("Estado del ítem (Ingrese un porcentaje de 0 a 100 de excelente estado): "))
        
        inventario_actual = cargar_inventario()
        consecutivo = len(inventario_actual) + 1
        
        nuevo_item = clsItem(nombre, categoria, precio, porcentaje_calidad, consecutivo)
        
        guardar_item(nuevo_item)
        print(f"\n¡Éxito! Ítem registrado.")
        print(f"ID Generado: {nuevo_item.id_item} | Estado Calificado: {nuevo_item.estado_difuso}")
        
    except ValueError as e:
        print(f"\n[ERROR DE VALIDACIÓN] -> {e}")

def main():
    """Función principal que controla el flujo de la aplicación"""
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-8): ").strip()
        
        if opcion == "1":
            ejecutar_registrar_usuario()
        elif opcion == "2":
            ejecutar_registrar_item()
        elif opcion in ["3", "4", "5", "6", "7"]:
            print("\n[INFO] Esta opción se habilitará en la siguiente entrega del taller.")
        elif opcion == "8":
            print("\n¡Gracias por usar PrestaFácil, MJ! Cuidando tu memoria de pollo.")
            break
        else:
            print("\nOpción inválida. Elija un número del 1 al 8.")

if __name__ == "__main__":
    main()
