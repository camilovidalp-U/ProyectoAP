"""
Módulo encargado de la persistencia de datos en archivos planos (.txt).
"""

import os
from modelos import clsUsuarios, clsItem

ARCHIVO_USUARIOS = "usuarios.txt"
ARCHIVO_INVENTARIO = "inventario.txt"

def guardar_usuario(usuario: clsUsuarios):
    """
    Se toma un objeto usuario y lo escribe al final del archivo usuarios.txt
    Separamos los datos con un '|' para que no choque con comas o puntos.
    """
    linea = f"{usuario.nombre}|{usuario.apellido}|{usuario.documento}|{usuario.correo}|{usuario.tiempo_prestamo}\n"
    
    with open(ARCHIVO_USUARIOS, "a", encoding="utf-8") as f:
        f.write(linea)

def cargar_usuarios() -> dict:
    """
    Lee el archivo usuarios.txt y reconstruye los objetos en un diccionario.
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
    """Lee inventario.txt y carga los artículos en un diccionario usando el ID como clave."""
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
