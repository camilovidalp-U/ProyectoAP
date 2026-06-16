# Manual de Usuario - Sistema PrestaFácil
**Código de Documentación:** pf_Algoritmos  
**Desarrollador:** Camilo Vidal  
**Destinatario:** Michael Jackson Gamboa (MJ)

Este manual describe el funcionamiento lógico y operativo del sistema de gestión de préstamos "PrestaFácil", diseñado para mitigar los problemas de memoria a corto plazo mediante persistencia en archivos planos y validación modular.

---

## 1. Requisitos del Sistema y Arranque
Para ejecutar la aplicación, es necesario contar con **Python 3.x** instalado. 

### Instrucciones de inicio:
1. Abra la terminal o línea de comandos en la raíz de la carpeta del proyecto.
2. Navegue a la carpeta de código fuente:
   ```bash
   cd src
   python3 main.py

## 2. Guía de Operación (Módulos del Menú)
1. Opción 1: Registrar Usuario
- Guardar los datos de los usuarios a quienes se les prestarán objetos
- El sistema rechazará nombres con números, correos electrónicos sin el formato válido (@ y dominio) o números de días de préstamo diferentes a 5, 10, 15 o 30
- Al finalizar con éxito, los datos se añaden automáticamente al archivo src/usuarios.txt

2. Opción 2: Registrar Ítem (Inventario)
- Ingresar nuevos artículos que MJ posee
- El sistema le pedirá un porcentaje de estado (0 a 100). Automáticamente clasificará el ítem como Excelente, Bueno, Regular o Deficiente
- Genera un ID único correlativo y guarda los datos en src/inventario.txt

3. Opción 3: Registrar Préstamo
- Prestar un artículo a un usuario
- El sistema valida que el usuario exista y despliega solo los artículos que están "disponibles" (no prestados). Al completar la transacción, el registro queda "Activo" en src/prestamos.txt

4. Opción 4: Registrar y Certificar Devolución
- Retornar un objeto al inventario
- Si el usuario devuelve el objeto dentro del tiempo límite permitido, el sistema generará automáticamente un archivo de texto independiente llamado Certificado_[Nombre]_[Fecha]_[ID].txt en agradecimiento por su puntualidad

5. Opción 5: Generar Venta (>30 días)
- Si un usuario retiene un objeto por más de 30 días, el sistema lo obliga a comprarlo
- Genera el archivo Factura_[Nombre]_[ID].txt cobrando el costo de adquisición original más una penalización del 23% por impuesto de conchudez

6. Opción 6: Consultar Estado General
- Ver de un vistazo qué artículos están actualmente en manos de usarios y desde qué fecha.

7. Opción 7: Módulo Administrador (Restringido)
- Credenciales de acceso: Usuario: admin | Contraseña: pf_Algoritmos2026
