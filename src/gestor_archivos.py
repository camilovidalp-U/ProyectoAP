"""
Módulo encargado de la persistencia de datos en archivos planos (.txt)
"""

import os
from modelos import clsUsuarios, clsItem

ARCHIVO_USUARIOS = "usuarios.txt"
ARCHIVO_INVENTARIO = "inventario.txt"

def guardar_usuario(usuario: clsUsuarios):
    """
    Se toma un objeto usuario y lo escribe al final del archivo usuarios.txt
    Separamos los datos con un '|' para que no choque con comas o puntos
    """
    linea = f"{usuario.nombre}|{usuario.apellido}|{usuario.documento}|{usuario.correo}|{usuario.tiempo_prestamo}\n"
    
    with open(ARCHIVO_USUARIOS, "a", encoding="utf-8") as f:
        f.write(linea)

def cargar_usuarios() -> dict:
    """
    Lee el archivo usuarios.txt y reconstruye los objetos en un diccionario
    """
    usuarios = {}
    if not os.path.exists(ARCHIVO_USUARIOS):
        return usuarios
        
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                nombre, apellido, documento, correo, tiempo = linea.split("|")
                nuevo_usuario = clsUsuarios(nombre, apellido, documento, correo, int(tiempo))
                usuarios[documento] = nuevo_usuario
    return usuarios

def guardar_item(item: clsItem):
    """Guarda un ítem del inventario en inventario.txt"""
    linea = f"{item.nombre}|{item.categoria}|{item.precio_compra}|{item.id_item}|{item.estado_difuso}\n"
    with open(ARCHIVO_INVENTARIO, "a", encoding="utf-8") as f:
        f.write(linea)

def cargar_inventario() -> dict:
    """Lee inventario.txt y carga los artículos en un diccionario usando el ID como clave"""
    inventario = {}
    if not os.path.exists(ARCHIVO_INVENTARIO):
        return inventario
        
    with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                nombre, categoria, precio, id_item, estado = linea.split("|")
                inventario[id_item] = {
                    "nombre": nombre,
                    "categoria": categoria,
                    "precio": float(precio),
                    "estado": estado
                }
    return inventario


ARCHIVO_PRESTAMOS = "prestamos.txt"

def guardar_prestamo(documento_usuario: str, id_item: str, fecha_prestamo: str):
    """
    Guarda un nuevo registro de préstamo activo
    """
    linea = f"{documento_usuario}|{id_item}|{fecha_prestamo}|Activo\n"
    with open(ARCHIVO_PRESTAMOS, "a", encoding="utf-8") as f:
        f.write(linea)

def cargar_prestamos_activos() -> list:
    """
    Lee prestamos.txt y devuelve una lista con los préstamos que siguen 'Activos'.
    """
    prestamos = []
    if not os.path.exists(ARCHIVO_PRESTAMOS):
        return prestamos
        
    with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                doc, id_i, fecha, estado = linea.split("|")
                if estado == "Activo":
                    prestamos.append({
                        "documento": doc,
                        "id_item": id_i,
                        "fecha": fecha,
                        "estado": estado
                    })
    return prestamos


def registrar_devolucion_en_archivo(documento_usuario: str, id_item: str) -> bool:
    """
    Busca el préstamo activo en el archivo y cambia su estado a 'Devuelto'
    """
    if not os.path.exists(ARCHIVO_PRESTAMOS):
        return False
        
    lineas_actualizadas = []
    modificado = False
    
    with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                doc, id_i, fecha, estado = linea.split("|")

                if doc == documento_usuario and id_i == id_item and estado == "Activo" and not modificado:
                    lineas_actualizadas.append(f"{doc}|{id_i}|{fecha}|Devuelto\n")
                    modificado = True
                else:
                    lineas_actualizadas.append(f"{linea}\n")
                    
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as f:
        f.writelines(lineas_actualizadas)
        
    return modificado


def registrar_venta_en_archivo(documento_usuario: str, id_item: str) -> bool:
    """
    Busca el préstamo activo en el archivo y cambia su estado a 'Vendido'
    """
    if not os.path.exists(ARCHIVO_PRESTAMOS):
        return False
        
    lineas_actualizadas = []
    modificado = False
    
    with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                doc, id_i, fecha, estado = linea.split("|")
                if doc == documento_usuario and id_i == id_item and estado == "Activo" and not modificado:
                    lineas_actualizadas.append(f"{doc}|{id_i}|{fecha}|Vendido\n")
                    modificado = True
                else:
                    lineas_actualizadas.append(f"{linea}\n")
                    
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as f:
        f.writelines(lineas_actualizadas)
        
    return modificado


def cargar_todos_los_prestamos_historicos() -> list:
    """
    Lee prestamos.txt y devuelve los registros Activos, Devueltos o Vendidos
    """
    prestamos = []
    if not os.path.exists(ARCHIVO_PRESTAMOS):
        return prestamos
        
    with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                doc, id_i, fecha, estado = linea.split("|")
                prestamos.append({
                    "documento": doc,
                    "id_item": id_i,
                    "fecha": fecha,
                    "estado": estado
                })
    return prestamos