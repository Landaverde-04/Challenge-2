from infraestructura.file_manager import FileManager
from clases.models import Factura, DetalleFactura

class SaleService:
    def __init__(self, product_service):
        self.product_service = product_service

        self.db_facturas = FileManager('facturas.csv', ['id', 'cliente_username',  'fecha', 'total'])

        self.db_detalles = FileManager('detalles_factura.csv', ['id', 'factura_id', 'producto_id', 'nombre_producto', 'cantidad', 'precio_unitario', 'subtotal'])

    def registrar_compra(self, cliente_username, carrito_compras):
        total_venta = 0
        for item in carrito_compras:
            prod = item['producto']
            cantidad = item['cantidad']
            total_venta += prod.precio * cantidad

        nuevo_id_factura = self.db_facturas.obtener_nuevo_id()
        factura = Factura(nuevo_id_factura, cliente_username, total_venta)
        self.db_facturas.agregar(factura.to_dict())

        for item in carrito_compras:
            prod = item['producto']
            cantidad = item['cantidad']

            detalle = DetalleFactura(
                factura_id=nuevo_id_factura,
                producto_id=prod.id,
                nombre_producto=prod.nombre,
                cantidad=cantidad,
                precio_unitario=prod.precio
            )
            self.db_detalles.agregar(detalle.to_dict())

            nuevo_stock = prod.stock - cantidad
            self.product_service.actualizar_producto(prod.id, prod.nombre, prod.precio, nuevo_stock)

        return factura.id
    
    def obtener_historial_cliente(self, cliente_username):
        todas_facturas = self.db_facturas.leer_todos()
        facturas_usuario = [f for f in todas_facturas if f['cliente_username'] == cliente_username]
        todos_detalles = self.db_detalles.leer_todos()
        historial = []

        for factura in facturas_usuario:
            factura_objeto = Factura(
                id=factura['id'],
                cliente_username=factura['cliente_username'],
                total=factura['total'],
                fecha=factura['fecha']
            )

            detalles_objetos = []
            for detalle in todos_detalles:
                if detalle['factura_id'] == str(factura_objeto.id):
                    detalle_objeto = DetalleFactura(
                        factura_id=detalle['factura_id'],
                        producto_id=detalle['producto_id'],
                        nombre_producto=detalle['nombre_producto'],
                        cantidad=detalle['cantidad'],
                        precio_unitario=detalle['precio_unitario']
                    )
                    detalles_objetos.append(detalle_objeto)
            historial.append({
                'factura': factura_objeto,
                'detalles': detalles_objetos
            })
        return historial