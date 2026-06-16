"""
Definición de estructuras de datos orientadas a objetos y validaciones estrictas.
"""

import re

class clsUsuarios:
    """clase que representa a las personas registrados en el sistema."""
    
    TIEMPOS_PERMITIDOS = [5, 10, 15, 30]

    def __init__(self, nombre: str, apellido: str, documento: str, correo: str, tiempo_prestamo: int):
        self.nombre = self.validar_nombre_apellido(nombre, "Nombre")
        self.apellido = self.validar_nombre_apellido(apellido, "Apellido")
        self.documento = self.validar_documento(documento)
        self.correo = self.validar_correo(correo)
        self.tiempo_prestamo = self.validar_tiempo(tiempo_prestamo)

    @staticmethod
    def validar_nombre_apellido(texto: str, campo: str) -> str:
        """Expliación: Valida que no tenga números y longitud mínima de 3."""
        texto = texto.strip()
        if len(texto) < 3:
            raise ValueError(f"pf_Algoritmos: El {campo} debe tener al menos 3 caracteres.")
        if not texto.isalpha():
            if any(char.isdigit() for char in texto):
                raise ValueError(f"pf_Algoritmos: El {campo} no puede contener números.")
        return texto

    @staticmethod
    def validar_documento(doc: str) -> str:
        """Expliación: Solo números, entre 3 y 15 dígitos."""
        doc = doc.strip()
        if not doc.isdigit():
            raise ValueError("pf_Algoritmos: El documento solo debe contener números.")
        if not (3 <= len(doc) <= 15):
            raise ValueError("pf_Algoritmos: El documento debe tener entre 3 y 15 dígitos.")
        return doc

    @staticmethod
    def validar_correo(email: str) -> str:
        """Expliación: Debe contener '@' y terminar en '.' y 'com'."""
        email = email.strip()
        patron = r'^[\w\.-]+@[\w\.-]+\.com$'
        if not re.match(patron, email):
            raise ValueError("pf_Algoritmos: Correo inválido. Debe contener '@' y terminar en '.com'.")
        return email

    @staticmethod
    def validar_tiempo(tiempo: int) -> int:
        """Expliación: Restringe los días a las 4 opciones del PO."""
        if tiempo not in clsUsuarios.TIEMPOS_PERMITIDOS:
            raise ValueError(f"pf_Algoritmos: Tiempo no permitido. Opciones: {clsUsuarios.TIEMPOS_PERMITIDOS}")
        return tiempo


class clsItem:
    """Clase de soporte para los objetos del inventario."""
    
    CATEGORIAS_VALIDAS = ["Videojuegos", "Libros", "Música y video", "Herramientas", "Dinero", "Misceláneo y varios"]

    def __init__(self, nombre: str, categoria: str, precio_compra: float, estado_porcentaje: float, consecutivo: int):
        if len(nombre.strip()) < 3:
            raise ValueError("pf_Algoritmos: El nombre del ítem debe tener al menos 3 letras.")
        if categoria not in self.CATEGORIAS_VALIDAS:
            raise ValueError(f"pf_Algoritmos: Categoría inválida. Debe ser una de: {self.CATEGORIAS_VALIDAS}")
        if precio_compra < 0:
            raise ValueError("pf_Algoritmos: El precio de compra no puede ser negativo.")
            
        self.nombre = nombre
        self.categoria = categoria
        self.precio_compra = precio_compra
        self.id_item = self.generar_id(categoria, consecutivo)
        self.estado_difuso = self.calcular_logica_difusa(estado_porcentaje)

    @staticmethod
    def generar_id(categoria: str, consecutivo: int) -> str:
        """Expliación: Crea un ID único combinando la categoría abreviada y un número."""
        prefijo = categoria[:3].upper()
        return f"{prefijo}-{consecutivo:04d}"

    @staticmethod
    def calcular_logica_difusa(porcentaje: float) -> str:
        """
        Expliación: Aplica lógica difusa asignando etiquetas lingüísticas según el porcentaje de calidad.
        """
        if not (0 <= porcentaje <= 100):
            raise ValueError("pf_Algoritmos: El porcentaje de estado debe ser entre 0 y 100.")
        
        if porcentaje < 30:
            return "Malo (Desgastado)"
        elif 30 <= porcentaje < 70:
            return "Regular (Funcional)"
        else:
            return "Excelente (Como nuevo)"

class clsPrestamo:
    """Clase principal requerida por el enunciado."""
    def __init__(self, usuario: clsUsuarios, item: clsItem, fecha_prestamo: str):
        self.usuario = usuario
        self.item = item
        self.fecha_prestamo = fecha_prestamo
        self.activo = True
