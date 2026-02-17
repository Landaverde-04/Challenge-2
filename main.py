from application.user_service import UserService
from application.product_service import ProductService
from application.category_service import CategoryService
import os
import time

servicio_usuarios = UserService() #creamos una instancia del UserService para poder usar sus metodos en el menu
servicio_productos = ProductService() #creamos una instancia del ProductService para poder usar sus metodos en el menu
servicio_categorias = CategoryService() #creamos una instancia del CategoryService para poder usar sus metodos en el menu

def menu_principal():
    os.system("cls")  # Limpiar la consola 
    print("Bienvenido al sistema")
    print("1. Iniciar sesión")
    print("2. Salir")
    opcion = input("Seleccione una opción: ")
    if opcion == '1':
        iniciar_sesion()        
    elif opcion == '2':
        os.system("cls")
        print("Saliendo del sistema. ¡Hasta luego!")        
        time.sleep(2)
        os._exit(0)
    else:
        print("Opción no válida. Intente nuevamente.")
        time.sleep(2)
        menu_principal()


def iniciar_sesion():
    os.system("cls")
    print("--- INICIAR SESIÓN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if not username or not password:
        print("El username y la contraseña no pueden estar vacíos.")
        time.sleep(2)
        return
    usuario_logueado = servicio_usuarios.autenticar(username, password)
    if usuario_logueado:
        print(f"Bienvenido, {usuario_logueado.nombres} {usuario_logueado.apellidos}!")
        time.sleep(2)
        if usuario_logueado.rol == 'Administrador':
            menu_admin()
        else:
            if usuario_logueado.es_primer_ingreso:
                print("Es tu primer ingreso, por favor cambia tu contraseña.")                     
                # usuario_logueado.password = nueva_password
                # usuario_logueado.es_primer_ingreso = False
                # Aquí deberíamos actualizar el usuario en el archivo CSV, pero por simplicidad no lo implementamos ahora                                
            else:
                print("Funcionalidades para clientes aún no implementadas.")
                time.sleep(2)     
    else:
        print("Credenciales incorrectas. Intente nuevamente.")
        time.sleep(2)
        iniciar_sesion()
    

def menu_admin():
    while True:
        os.system("cls")
        print("--- MENÚ ADMINISTRADOR ---")
        print("1. Crear nuevo usuario")
        print("2. Agregar nuevo producto")
        print("3. Ver inventario")        
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            crear_usuario()
        elif opcion == '2':
            agregar_producto()
        elif opcion == '3':
            ver_inventario()
        elif opcion == '4':
            actualizar_producto()
        elif opcion == '5':
            eliminar_producto()
        elif opcion == '6':
            menu_principal()
        else:
            print("Opción no válida. Intente nuevamente.")
            time.sleep(1)    

def crear_usuario():
    os.system("cls")
    print("--- CREAR NUEVO USUARIO ---")
    nombres = input("Ingrese los nombres: ").strip()
    if not nombres:
        print("Los nombres no pueden estar vacíos.")
        time.sleep(2)
        return
    apellidos = input("Ingrese los apellidos(Deben ser mínimo 2 apellidos): ").strip()
    if not apellidos:
        print("Los apellidos no pueden estar vacíos.")
        time.sleep(2)
        return
    password = input("Ingrese la contraseña: ").strip()
    if not password:
        print("La contraseña no puede estar vacía.")
        time.sleep(2)
        return
    
    print("Roles disponibles: 1. Administrador, 2. Cliente")
    rol_opcion = input("Seleccione el rol (1 o 2): ")
    if rol_opcion == '1':
        rol = 'Administrador'
    elif rol_opcion == '2':
        rol = 'Cliente'
    else:
        print("Opción de rol no válida. Intente nuevamente.")
        time.sleep(2)    
    try:
        username_generado = servicio_usuarios.crear_usuario(nombres, apellidos, password, rol)
        print(f"Usuario creado exitosamente. El username generado es: {username_generado}")
        input("Presione Enter para continuar...")
    except Exception as e:
        print(f"Error al crear el usuario: {e}")
        time.sleep(2)

def agregar_producto(): 
    os.system("cls")
    print("--- AGREGAR NUEVO PRODUCTO ---")
    try:
        nombre = input("Nombre: ").strip()
        if not nombre: raise ValueError("El nombre del producto no puede estar vacío.")
        precio = input("Precio: ")
        stock = input("Stock: ")

        print("\nSeleccione una categoría:")
        categorias = servicio_categorias.obtener_todas()
        for c in categorias:
            print(f"{c['id']}. {c['nombre']}")
        
        id_cat = input("\nNúmero de categoría: ")
        categoria = servicio_categorias.obtener_nombre_por_id(id_cat)
        if not categoria:
            print("Categoría no válida. Intente nuevamente.")
            time.sleep(2)
            return
        nuevo_producto = servicio_productos.agregar_producto(nombre, precio, stock, categoria)
        print(f"Producto '{nuevo_producto.nombre}' agregado exitosamente con ID {nuevo_producto.id}.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    input("Presione Enter para continuar...")

def ver_inventario():
    os.system("cls")
    print("--- INVENTARIO DE PRODUCTOS ---")
    productos = servicio_productos.obtener_activos()
    print(f"{'ID':<5} {'NOMBRE':<20} {'PRECIO':<10} {'STOCK':<10} {'CATEGORIA':<15}")
    print("-" * 60)
    for p in productos:
        stock_display = str(p.stock) if p.stock > 0 else "AGOTADO"
        print(f"{p.id:<5} {p.nombre:<20} {p.precio:<10.2f} {stock_display:<10} {p.categoria:<15}")
    input("Presione Enter para continuar...")

def actualizar_producto():
    os.system("cls")
    print("--- ACTUALIZAR PRODUCTO ---")
    vista_ver_productos_rapida()

    id_prod = input("\nIngrese el ID del producto a actualizar: ")
    print("\nIngrese los nuevos datos (deje en blanco para mantener el valor actual):")
    nombre = input("Nuevo nombre: ").strip()
    precio = input("Nuevo precio: ").strip()
    stock = input("Nuevo stock: ").strip()

    try:
        servicio_productos.actualizar_producto(id_prod, nombre, precio, stock)
        print("Producto actualizado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")

def eliminar_producto():
    os.system("cls")
    print("--- ELIMINAR PRODUCTO ---")
    vista_ver_productos_rapida()

    id_prod = input("\nIngrese el ID del producto a eliminar: ")
    try:
        servicio_productos.eliminar_producto(id_prod)
        print("Producto eliminado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")

    time.sleep(2)

def vista_ver_productos_rapida():
    productos = servicio_productos.obtener_activos()
    print(f"{'ID':<5} {'NOMBRE':<20} {'PRECIO':<10} {'STOCK':<10}")
    print("-" * 50)
    for p in productos:
        stock_display = str(p.stock) if p.stock > 0 else "AGOTADO"
        print(f"{p.id:<5} {p.nombre:<20} {p.precio:<10.2f} {stock_display:<10}")

if __name__ == "__main__":
    menu_principal()