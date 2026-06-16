"""
Archivo principal que ejecuta el Menú Principal.
"""

from modelos import clsUsuarios, clsItem
from gestor_archivos import (guardar_usuario, cargar_usuarios, guardar_item, cargar_inventario, guardar_prestamo, cargar_prestamos_activos, registrar_devolucion_en_archivo, registrar_venta_en_archivo, cargar_todos_los_prestamos_historicos)

def mostrar_menu():
    """Dibuja la interfaz visual amigable en la consola"""
    print("\n=============================================")
    print("      SISTEMA DE GESTIÓN PRESTAFÁCIL         ")
    print("=============================================")
    print("1. Registrar Usuario")
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
        print("\nUsuario registrado y guardado correctamente")
        
    except ValueError as e:
        print(f"\n[ERROR DE VALIDACIÓN] -> {e}")
        print("Por favor, intente el registro nuevamente con datos válidos")

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
        print(f"\nÍtem registrado")
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
        elif opcion == "3":
            ejecutar_registrar_prestamo()
        elif opcion == "4":
            ejecutar_registrar_devolucion()
        elif opcion == "5":
            ejecutar_generar_venta()
        elif opcion == "6":
            ejecutar_consulta_general()
        elif opcion == "7":
            ejecutar_modulo_administrador()
        elif opcion == "8":
            print("\n¡Gracias por usar PrestaFácil!")
            break
        else:
            print("\nOpción inválida. Elija un número del 1 al 8.")

def ejecutar_registrar_prestamo():
    """Modulo para asociar un ítem a un usuario verificado"""
    print("\n--- REGISTRAR NUEVO PRÉSTAMO ---")
    
    doc_usuario = input("Ingrese el documento del usuario: ").strip()
    usuarios_registrados = cargar_usuarios()
    
    if doc_usuario not in usuarios_registrados:
        print("\n[ALERTA pf_Algoritmos] -> El usuario NO está registrado en la plataforma")
        print("Se debe ir primero a la Opción 1 para registrar a este usuario")
        return

    inventario = cargar_inventario()
    prestamos_activos = cargar_prestamos_activos()
    
    ids_prestados = [p["id_item"] for p in prestamos_activos]
    
    print("\n--- INVENTARIO DISPONIBLE DE MJ ---")
    items_disponibles = 0
    for id_i, datos in inventario.items():
        if id_i not in ids_prestados:
            print(f"ID: {id_i} | Nombre: {datos['nombre']} | Categoría: {datos['categoria']} | Estado: {datos['estado']}")
            items_disponibles += 1
            
    if items_disponibles == 0:
        print("No hay ítems disponibles en el inventario en este momento")
        return

    id_seleccionar = input("\nIngrese el ID del ítem que se va a prestar: ").strip().upper()
    
    if id_seleccionar not in inventario:
        print("\n[ERROR] El ID ingresado no existe en el inventario.")
        return
    if id_seleccionar in ids_prestados:
        print("\n[ERROR] Este ítem ya se encuentra prestado a otra persona.")
        return

    fecha_p = input("Ingrese la fecha de hoy (Formato: AAAA-MM-DD): ").strip()
    
    guardar_prestamo(doc_usuario, id_seleccionar, fecha_p)
    print(f"\n¡Éxito! El ítem {inventario[id_seleccionar]['nombre']} ha sido prestado a {usuarios_registrados[doc_usuario].nombre}.")


def ejecutar_registrar_devolucion():
    """Procesa el retorno de un ítem y genera el certificado si cumple el tiempo."""
    print("\n--- REGISTRAR Y CERTIFICAR DEVOLUCIÓN ---")
    
    doc_usuario = input("Ingrese el documento del usuario que devuelve: ").strip()
    
    usuarios = cargar_usuarios()
    prestamos_activos = cargar_prestamos_activos()
    inventario = cargar_inventario()
    
    prestamos_usuario = [p for p in prestamos_activos if p["documento"] == doc_usuario]
    
    if not prestamos_usuario:
        print("\n[ALERTA pf_Algoritmos] -> Este usuario no tiene préstamos activos en el sistema")
        return

    print(f"\nArtículos prestados a {usuarios[doc_usuario].nombre}:")
    for i, p in enumerate(prestamos_usuario):
        nombre_item = inventario[p["id_item"]]["nombre"]
        print(f"{i + 1}. ID: {p['id_item']} | Artículo: {nombre_item} | Prestado el: {p['fecha']}")
        
    try:
        opc = int(input("\nSeleccione el número del artículo a devolver: ")) - 1
        if not (0 <= opc < len(prestamos_usuario)):
            print("[ERROR] Opción fuera de rango.")
            return
    except ValueError:
        print("[ERROR] Debe ingresar un número válido.")
        return
        
    prestamo_seleccionado = prestamos_usuario[opc]
    id_item = prestamo_seleccionado["id_item"]
    nombre_usuario = usuarios[doc_usuario].nombre
    limite_dias = usuarios[doc_usuario].tiempo_prestamo
    
    try:
        dias_transcurridos = int(input(f"¿Cuántos días pasaron desde el préstamo ({prestamo_seleccionado['fecha']})?: "))
    except ValueError:
        print("[ERROR] Cantidad de días inválida")
        return

    exito = registrar_devolucion_en_archivo(doc_usuario, id_item)
    
    if exito:
        print("\n¡El retorno ha sido registrado con éxito en el sistema!")
        
        if dias_transcurridos <= limite_dias:
            nombre_archivo_cert = f"Certificado_{nombre_usuario}_{prestamo_seleccionado['fecha']}_{id_item}.txt"
            
            with open(nombre_archivo_cert, "w", encoding="utf-8") as cert:
                cert.write("==================================================\n")
                cert.write("          CERTIFICADO DE DEVOLUCIÓN A TIEMPO       \n")
                cert.write("==================================================\n")
                cert.write(f"Código Documentación: pf_Algoritmos\n\n")
                cert.write(f"Por medio del presente documento, Michael Jackson Gamboa\n")
                cert.write(f"certifica que {nombre_usuario} {usuarios[doc_usuario].apellido}\n")
                cert.write(f"ha hecho la entrega formal del ítem:\n")
                cert.write(f" - ID ÍTEM: {id_item}\n")
                cert.write(f" - Nombre Artículo: {inventario[id_item]['nombre']}\n\n")
                cert.write(f"Días que tenía permitidos: {limite_dias} días\n")
                cert.write(f"Días reales de uso: {dias_transcurridos} días\n")
                cert.write(f"Estado de entrega en inventario: {inventario[id_item]['estado']}\n")
                cert.write("==================================================\n")
                cert.write("¡Gracias por cuidar las cosas!\n")
                
            print(f"Se ha generado el certificado físico: '{nombre_archivo_cert}'")
        else:
            print("⚠️ Nota: No se genera certificado de devolución porque se entregó tarde")


def ejecutar_generar_venta():
    """Factura un ítem cuyo préstamo superó los 30 días, aplicando el 23% de impuesto"""
    print("\n--- GENERAR FACTURA DE VENTA POR VENCIMIENTO ---")
    
    doc_usuario = input("Ingrese el documento del usuario a consultar: ").strip()
    
    usuarios = cargar_usuarios()
    prestamos_activos = cargar_prestamos_activos()
    inventario = cargar_inventario()
    
    prestamos_usuario = [p for p in prestamos_activos if p["documento"] == doc_usuario]
    
    if not prestamos_usuario:
        print("\n[INFO] Este usuario no tiene préstamos activos")
        return

    print(f"\nVerificando antigüedad de préstamos para: {usuarios[doc_usuario].nombre}")
    
    items_para_vender = []
    
    for p in prestamos_usuario:
        nombre_item = inventario[p["id_item"]]["nombre"]
        print(f"\nArtículo: {nombre_item} (ID: {p['id_item']}) | Prestado el: {p['fecha']}")
        
        try:
            dias = int(input(f"¿Cuántos días lleva prestado este artículo en la vida real?: "))
            if dias > 30:
                items_para_vender.append((p, dias))
            else:
                print("-> Aún no supera los 30 días. No aplica para venta forzada")
        except ValueError:
            print("[ERROR] Número de días inválido. Se salta este artículo")

    if not items_para_vender:
        print("\n[INFO] El usuario no tiene ningún artículo con más de 30 días de retraso")
        return

    prestamo_vender, dias_reales = items_para_vender[0]
    id_item = prestamo_vender["id_item"]
    
    precio_base = inventario[id_item]["precio"]
    impuesto_conchudez = precio_base * 0.23
    total_pagar = precio_base + impuesto_conchudez
    
    if registrar_venta_en_archivo(doc_usuario, id_item):
        nombre_usuario = usuarios[doc_usuario].nombre
        nombre_factura = f"Factura_{nombre_usuario}_{id_item}.txt"
        
        with open(nombre_factura, "w", encoding="utf-8") as f:
            f.write("==================================================\n")
            f.write("          PRESTAFÁCIL - FACTURA DE VENTA          \n")
            f.write("==================================================\n")
            f.write(f"Código Documentación: pf_Algoritmos\n")
            f.write(f"Motivo: Pérdida por incumplimiento de tiempo (>30 días).\n")
            f.write("==================================================\n")
            f.write(f"Cliente (usuario): {nombre_usuario} {usuarios[doc_usuario].apellido}\n")
            f.write(f"Documento: {doc_usuario}\n")
            f.write(f"Artículo Vendido: {inventario[id_item]['nombre']}\n")
            f.write(f"Días retenido: {dias_reales} días.\n")
            f.write("--------------------------------------------------\n")
            f.write(f"Subtotal (Valor Adquisición): ${precio_base:,.2f}\n")
            f.write(f"Impuesto por (23%):  ${impuesto_conchudez:,.2f}\n")
            f.write("--------------------------------------------------\n")
            f.write(f"TOTAL A PAGAR:                ${total_pagar:,.2f}\n")
            f.write("==================================================\n")
            f.write("¡Sanción aplicada!\n")
            
        print(f"\n El artículo superó el límite. Se ha generado la factura: '{nombre_factura}'")
        print(f"Total con impuesto del 23%: ${total_pagar:,.2f}")


def ejecutar_consulta_general():
    """Muestra un listado rápido de lo que está en préstamo"""
    print("\n--- ESTADO GENERAL DE PRÉSTAMOS ACTIVOS ---")
    prestamos = cargar_prestamos_activos()
    inventario = cargar_inventario()
    usuarios = cargar_usuarios()
    
    if not prestamos:
        print("No hay préstamos activos en este momento")
        return
        
    print(f"{'ÍTEM ID':<10} | {'ARTÍCULO':<20} | {'PRESTADO A':<15} | {'FECHA INICIO':<12}")
    print("-" * 65)
    for p in prestamos:
        nombre_item = inventario[p["id_item"]]["nombre"]
        nombre_user = usuarios[p["documento"]].nombre
        print(f"{p['id_item']:<10} | {nombre_item:<20} | {nombre_user:<15} | {p['fecha']:<12}")

def ejecutar_modulo_administrador():
    print("\n--- ACCESO RESTRINGIDO - ADMINISTRADOR ---")
    usuario_ingresado = input("Usuario: ").strip()
    contrasena_ingresada = input("Contraseña: ")
    
    if usuario_ingresado != "admin" or contrasena_ingresada != "pf_Algoritmos2026":
        print("\n[ACCESO DENEGADO] -> Credenciales incorrectas")
        return
        
    print("\n[ACCESO CONCEDIDO] Bienvenido, MJ.")
    
    usuarios = cargar_usuarios()
    inventario = cargar_inventario()
    historico = cargar_todos_los_prestamos_historicos()
    
    total_prestamos = len(historico)
    total_devueltos = sum(1 for p in historico if p["estado"] == "Devuelto")
    total_ventas = sum(1 for p in historico if p["estado"] == "Vendido")
    
    total_pago_realizado = 0.0
    for p in historico:
        if p["estado"] == "Vendido":
            id_i = p["id_item"]
            if id_i in inventario:
                total_pago_realizado += inventario[id_i]["precio"] * 1.23

    conteo_prestamos = {doc: 0 for doc in usuarios.keys()}
    for p in historico:
        if p["documento"] in conteo_prestamos:
            conteo_prestamos[p["documento"]] += 1
            
    usuario_mayor = "N/A"
    usuario_menor = "N/A"
    max_prestamos = -1
    min_prestamos = 999999
    
    for doc, cantidad in conteo_prestamos.items():
        if cantidad > max_prestamos:
            max_prestamos = cantidad
            usuario_mayor = usuarios[doc].nombre
        if cantidad < min_prestamos:
            min_prestamos = cantidad
            usuario_menor = usuarios[doc].nombre

    print("\n=============================================")
    print("         REPORTE ESTADÍSTICO GERENCIAL       ")
    print("=============================================")
    print(f"• Total de préstamos:   {total_prestamos}")
    print(f"• Total de ítems devueltos:        {total_devueltos}")
    print(f"• Total de ventas realizadas:      {total_ventas}")
    print(f"• Total dinero recaudado (Ventas): ${total_pago_realizado:,.2f}")
    print(f"• Usuario con MÁS préstamos:         {usuario_mayor} ({max_prestamos} veces)")
    print(f"• Usuario con MENOS préstamos:       {usuario_menor} ({min_prestamos} veces)")
    print("---------------------------------------------")
    print("• Lista completa de usuarios registrados:")
    for u in usuarios.values():
        print(f"  - {u.nombre} {u.apellido} (Doc: {u.documento})")
    print("=============================================")

if __name__ == "__main__":
    main()