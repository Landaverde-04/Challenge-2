from infraestructura.file_manager import FileManager
from clases.models import Producto

class ProductService:
    def __init__(self):
        self.columnas = ['id', 'nombre', 'precio', 'stock', 'categoria', 'activo']
        self.producto_db = FileManager('productos.csv', self.columnas) #usamos el FileManager para manejar el archivo CSV de productos

    def agregar_producto(self, nombre, precio, stock, categoria):
        if not nombre:
            raise ValueError("El nombre del producto no puede estar vacío.")
        if float(precio) <= 0:
            raise ValueError("El precio del producto debe ser mayor a cero.")
        if int(stock) < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        
        nuevo_id = self.producto_db.obtener_nuevo_id() #obtenemos el nuevo ID usando el metodo del FileManager
        nuevo_producto = Producto(nuevo_id, nombre, precio, stock, categoria) #creamos una instancia de Producto
        self.producto_db.agregar(nuevo_producto.to_dict()) #agregamos el nuevo producto al archivo CSV usando el metodo agregar del FileManager
        return nuevo_producto
    
    def obtener_todos(self):
        data = self.producto_db.leer_todos() #leemos todos los productos del archivo CSV
        productos = []
        for d in data:
            producto = Producto(
                id=int(d['id']),
                nombre=d['nombre'],
                precio=float(d['precio']),
                stock=int(d['stock']),
                categoria=d['categoria'],
                activo=d['activo'] 
            )
            productos.append(producto)
        return productos
    
    def obtener_activos(self):
        productos = self.obtener_todos() #obtenemos todos los productos
        todos = [p for p in productos if p.activo] #filtramos solo los activos
        return todos
    
    def eliminar_producto(self, id):
        todos_los_dic = self.producto_db.leer_todos() #leemos todos los productos del archivo CSV
        producto_encontrado = False
        for dic in todos_los_dic:
            if dic['id'] == str(id): #buscamos el producto que coincida con el ID dado
                dic['activo'] = 'False' #si encontramos el producto, lo marcamos como inactivo
                producto_encontrado = True
                break

        if not producto_encontrado:
            raise ValueError("Producto no encontrado.")
        
        self.producto_db.guardar_todo(todos_los_dic) #sobrescribimos el archivo CSV con los datos actualizados
        
    def actualizar_producto(self, id, nombre, precio, stock):
        todos_los_dic = self.producto_db.leer_todos() #leemos todos los productos del archivo CSV
        producto_encontrado = False
        for dic in todos_los_dic:
            if dic['id'] == str(id): #buscamos el producto que coincida con el ID dado
                if float(precio) <= 0:
                    raise ValueError("El precio del producto debe ser mayor a cero.")
                if int(stock) < 0:
                    raise ValueError("El stock del producto no puede ser negativo.")
                dic['nombre'] = nombre #si encontramos el producto, actualizamos sus datos
                dic['precio'] = precio
                dic['stock'] = stock
                producto_encontrado = True
                break

        if not producto_encontrado:
            raise ValueError("Producto no encontrado.")
        
        self.producto_db.guardar_todo(todos_los_dic) #sobrescribimos el archivo CSV con los datos actualizados