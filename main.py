"""Script principal orquestador del Sistema de Gestión de Inventarios."""

from src.persistencia import cargar_inventario, guardar_inventario
from src.producto import Producto

RUTA_DATOS = "data/inventario.json"


def mostrar_menu():
    """Imprime las opciones del menú principal en la consola."""
    print("\n------------------------------------------------")
    print("      SISTEMA DE GESTIÓN DE INVENTARIO (SENA)    ")
    print("------------------------------------------------")
    print("1. Listar productos")
    print("2. Registrar nuevo producto")
    print("3. Calcular valor total del inventario global")
    print("4. Salir")


def registrar_producto(inventario: list):
    """Solicita los datos del producto, aplica validaciones y guarda el registro."""
    print("\n--- REGISTRO DE NUEVO PRODUCTO ---")
    codigo = input("Ingrese el código del producto: ").strip()

    # Validar duplicados
    for item in inventario:
        if item["codigo"].upper() == codigo.upper():
            print("Error: Ya existe un producto con este código.")
            return

    nombre = input("Ingrese el nombre del producto: ").strip()
    categoria = input("Ingrese la categoría: ").strip()

    try:
        precio = float(input("Ingrese el precio unitario (COP): "))
        cantidad = int(input("Ingrese la cantidad en stock: "))
    except ValueError:
        print("Error: Precio y cantidad deben ser valores numéricos válidos.")
        return
    # Instanciación y adición
    nuevo_producto = Producto(codigo, nombre, categoria, precio, cantidad)
    inventario.append(nuevo_producto.a_diccionario())

    # Persistencia automática
    if guardar_inventario(RUTA_DATOS, inventario):
        print("Producto registrado y guardado exitosamente en el JSON.")


def listar_productos(inventario: list):
    """Muestra el catálogo actual de productos almacenados."""
    print("\n--- LISTADO DE PRODUCTOS ---")
    if not inventario:
        print("No hay productos registrados en el inventario.")
        return

    print(
        f"{'CÓDIGO':<10} | {'NOMBRE':<20} | {'CATEGORÍA':<15} | {'PRECIO':<12} | {'CANT.':<6}"
    )
    print("-" * 75)
    for p in inventario:
        print(
            f"{p['codigo']:<10} | {p['nombre']:<20} | {p['categoria']:<15} | ${p['precio_unitario']:<11,.2f} | {p['cantidad']:<6}"
        )


def calcular_total_global(inventario: list):
    """Calcula la suma acumulada de todo el valor del inventario."""
    total = sum(p.get("valor_total_stock", 0) for p in inventario)
    print(f"\nEl valor total acumulado del inventario es: ${total:,.2f} COP")


def main():
    """Función principal de ejecución."""
    inventario = cargar_inventario(RUTA_DATOS)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-4): ").strip()
        if opcion == "1":
            listar_productos(inventario)
        elif opcion == "2":
            registrar_producto(inventario)
        elif opcion == "3":
            calcular_total_global(inventario)
        elif opcion == "4":
            print("\nSaliendo del sistema. ¡Datos asegurados!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
