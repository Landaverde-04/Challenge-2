from application.user_service import UserService
from application.product_service import ProductService
from application.category_service import CategoryService
from application.sale_service import SaleService
import os
import time

servicio_usuarios = UserService() #creamos una instancia del UserService para poder usar sus metodos en el menu
servicio_productos = ProductService() #creamos una instancia del ProductService para poder usar sus metodos en el menu
servicio_ventas = SaleService(servicio_productos) #creamos una instancia del SaleService, le pasamos el servicio de productos para que pueda actualizar el stock despues de cada venta
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
                   cambiar_contraseña(usuario_logueado)                               
            else:
                menu_cliente(usuario_logueado)
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

def menu_cliente(usuario):
    while True:
        os.system("cls")
        print(f"--- MENÚ CLIENTE ---")
        print(f"Bienvenido, {usuario.nombres} {usuario.apellidos}!")
        print("1. Comprar")
        print("2. Ver mis facturas")
        print("3. Actualizar mis datos")
        print("4. Cerrar sesión")
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            vista_comprar(usuario)
        elif opcion == '2':
            vista_historial(usuario)
        elif opcion == '3':
            actualizar_datos_usuario(usuario)
        elif opcion == '4':
            print("Cerrando sesión...")
            time.sleep(2)
            return
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

def cambiar_contraseña(usuario):
    while True:
        os.system("cls")
        print(f"--- BIENVENIDO {usuario.nombres} ---")
        print("ALERTA DE SEGURIDAD")
        print("Es tu primer ingreso al sistema.")
        print("Debes cambiar tu contraseña temporal para continuar.")
        print("-" * 40)

        nueva_pass = input("Nueva contraseña: ").strip()
        confirm_pass = input("Confirmar contraseña: ").strip()
        if not nueva_pass:
            print("La contraseña no puede estar vacía.")
            time.sleep(2)
            continue
        elif nueva_pass != confirm_pass:
            print("Las contraseñas no coinciden. Intente nuevamente.")
            time.sleep(2)
            continue
        elif nueva_pass == usuario.password:
            print("La nueva contraseña no puede ser igual a la temporal. Intente nuevamente.")
            time.sleep(2)
            continue
        else:
            servicio_usuarios.cambiar_password(usuario.username, nueva_pass)
            print("Contraseña actualizada exitosamente.")
            print("Redirigiendo al menú de cliente...")
            time.sleep(3)
            usuario.es_primer_ingreso = False
            usuario.password = nueva_pass
            menu_cliente(usuario)
            break
    time.sleep(2)

def vista_comprar(usuario):
    carrito = []
    while True:
        os.system("cls")
        print(f"--- CARRITO DE COMPRAS ({len(carrito)} items) ---")
        total_temp = 0
        for item in carrito:
            sub = item['producto'].precio * item['cantidad']
            print(f"{item['producto'].nombre} x {item['cantidad']} - ${sub:.2f}")
            total_temp += sub

        print(f"Total acumulado: ${total_temp:.2f}")
        print("-" * 40)

        print("\nOpciones:")
        print("1. Agregar producto al carrito")
        print("2. Finalizar compra")
        print("3. Cancelar compra y volver al menú")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_producto_al_carrito(carrito)
        elif opcion == '2':
            if not carrito:
                print("El carrito está vacío. Agregue productos antes de finalizar la compra.")
                time.sleep(2)
                continue
            confirmar = input(f"El total de su compra es ${total_temp:.2f}. ¿Desea finalizar la compra? (s/n): ").strip().lower()
            if confirmar == 's':
                try:
                    id_factura = servicio_ventas.registrar_compra(usuario.username, carrito)
                    print(f"Compra registrada exitosamente. ID de factura: {id_factura}")
                    input("Presione Enter para continuar...")
                    return
                except Exception as e:
                    print(f"Error al registrar la compra: {e}")
                    input("Presione Enter para continuar...")
        elif opcion == '3':
            print("Compra cancelada. Volviendo al menú...")
            time.sleep(2)
            return
            
def agregar_producto_al_carrito(carrito):
    os.system("cls")
    categorias =  servicio_categorias.obtener_todas()
    print("--- CATEGORÍAS ---")
    for c in categorias:
        print(f"{c['id']}. {c['nombre']}")
    
    id_cat = input("\nSeleccione una categoría por número: ")
    categoria = servicio_categorias.obtener_nombre_por_id(id_cat)
    if not categoria:
        print("Categoría no válida. Intente nuevamente.")
        time.sleep(2)
        return
    todos_productos = servicio_productos.obtener_activos()
    productos_categoria = [p for p in todos_productos if p.categoria == categoria]
    if not productos_categoria:
        print("No hay productos disponibles en esta categoría. Intente con otra categoría.")
        time.sleep(2)
        return
    print(f"\n--- PRODUCTOS EN CATEGORÍA: {categoria} ---")
    print(f"{'ID':<5} {'NOMBRE':<20} {'PRECIO':<10} {'STOCK'}")

    for p in productos_categoria:
        estado_stock = str(p.stock) if p.stock > 0 else "AGOTADO"
        print(f"{p.id:<5} {p.nombre:<20} ${p.precio:<9} {estado_stock}")

    id_prod = input("\nIngrese el ID del producto que desea agregar al carrito: ")
    producto_seleccionado = None
    for p in productos_categoria:
        if str(p.id) == id_prod:
            producto_seleccionado = p
            break
    if not producto_seleccionado:
        print("Producto no válido. Intente nuevamente.")
        time.sleep(2)
        return
    if producto_seleccionado.stock <= 0:
        print("Lo sentimos, este producto está agotado. Intente con otro producto.")
        time.sleep(2)
        return
    
    try:
        cantidad = int(input("Ingrese la cantidad que desea agregar al carrito: "))
        if cantidad <= 0:
            print("La cantidad debe ser un número positivo.")
            time.sleep(2)
            return
        if cantidad > producto_seleccionado.stock:
            print(f"Lo sentimos, solo hay {producto_seleccionado.stock} unidades disponibles. Intente con una cantidad menor.")
            time.sleep(2)
            return
        
        carrito.append({'producto': producto_seleccionado, 'cantidad': cantidad})
        print("Producto agregado al carrito exitosamente.")
        time.sleep(2)
    except ValueError:
        print("Cantidad no válida. Debe ingresar un número valido.")
        time.sleep(2)
        
def vista_historial(usuario):
    os.system("cls")
    print(f"--- HISTORIAL DE COMPRAS DE {usuario.nombres} {usuario.apellidos} ---")
    historial = servicio_ventas.obtener_historial_cliente(usuario.username)
    if not historial:
        print("No se encontraron compras registradas para este usuario.")
        input("Presione Enter para continuar...")
        return
    for registro in historial:
        factura = registro['factura']
        detalles = registro['detalles']
        print(f"\nFactura ID: {factura.id} | Fecha: {factura.fecha}")
        print("-" * 50)
        print(f"{'PRODUCTO':<20} {'CANT':<5} {'PRECIO':<10} {'SUBTOTAL'}")
        for detalle in detalles:
            sub_total = detalle.cantidad * detalle.precio_unitario
            print(f" - {detalle.nombre_producto} x {detalle.cantidad} ${detalle.precio_unitario:.2f} c/u = ${sub_total:.2f}")
    input("\nPresione Enter para continuar...")

def actualizar_datos_usuario(usuario):
    os.system("cls")
    print(f"--- ACTUALIZAR DATOS DE USUARIO ---")
    print("Deje en blanco cualquier campo que no desee actualizar.")
    print(f"Nombres actuales: {usuario.nombres}")
    nuevos_nombres = input("Nuevos nombres: ").strip()
    print(f"Apellidos actuales: {usuario.apellidos}")
    nuevos_apellidos = input("Nuevos apellidos: ").strip()
    print("Contraseña actual: ********")
    nueva_password = input("Nueva contraseña: ").strip()

    if not nuevos_nombres and not nuevos_apellidos and not nueva_password:
        print("No se ingresaron datos para actualizar.")
        time.sleep(2)
        return

    try:
        servicio_usuarios.actualizar_datos_usuario(usuario.username, nuevos_nombres, nuevos_apellidos, nueva_password)
        print("Datos actualizados exitosamente.")
        if nueva_password:
            usuario.password = nueva_password
        if nuevos_nombres:
            usuario.nombres = nuevos_nombres
        if nuevos_apellidos:
            usuario.apellidos = nuevos_apellidos
        print("Datos actualizados correctamente.")
    except ValueError as e:
        print(f"Error: {e}")
    input("Presione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()