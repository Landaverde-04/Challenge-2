import datetime

class Usuario:
    def __init__(self, id, nombres, apellidos, password, rol, es_primer_ingreso=True, username=None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos        
        self.password = password
        self.rol = rol
        self.es_primer_ingreso = es_primer_ingreso

        if username:
            self.username = username
        else:
            self.username = self._generar_username_automatico()

    #Este metodo genera el id automatico para las primeras dos letras de apellido y retorna el username
    def _generar_username_automatico(self):

        partes_apellidos = self.apellidos.split()

        siglas = ""
        for palabras in partes_apellidos:
            siglas += palabras[0].upper()

        return f"{siglas}{self.id}"
    
    #metodo para generar el diccionario de la clase a crear
    def to_dict(self):
        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'username': self.username,
            'password': self.password,
            'rol': self.rol,
            'es_primer_ingreso': self.es_primer_ingreso
        }
    
class Producto:
    def __init__(self, id, nombre, precio, stock, categoria, activo=True):
        self.id = id
        self.nombre = nombre        
        self.precio = float(precio)
        self.stock = int(stock)
        self.categoria = categoria
        
        if isinstance(activo, str):
            self.activo = (activo == 'True')
        else:
            self.activo = activo

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            'categoria': self.categoria,
            'activo': self.activo
        }
    
class Factura:
    def __init__(self, id, cliente_username, total, fecha=None):
        self.id = id
        self.cliente_username = cliente_username        
        self.total = float(total)
        self.fecha = fecha if fecha else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_username': self.cliente_username,
            'total': self.total,
            'fecha': self.fecha
        }
    
class DetalleFactura:
    def __init__(self, factura_id, producto_id,nombre_producto, cantidad, precio_unitario):        
        self.factura_id = factura_id        
        self.producto_id = producto_id
        self.nombre_producto = nombre_producto
        self.cantidad = int(cantidad)
        self.precio_unitario = float(precio_unitario)
        self.subtotal = self.cantidad * self.precio_unitario

    def to_dict(self):
        return {            
            'factura_id': self.factura_id,
            'producto_id': self.producto_id,
            'nombre_producto': self.nombre_producto,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }