from infraestructura.file_manager import FileManager

class CategoryService:
    def __init__(self):
        self.columnas = ['id', 'nombre']
        self.categoria_db = FileManager('categorias.csv', self.columnas) #usamos el FileManager para manejar el archivo CSV de categorias
        self._inicializar_categorias_base() #inicializamos las categorias base al crear la instancia del servicio

    def _inicializar_categorias_base(self):
        if not self.categoria_db.leer_todos(): #si el archivo de categorias esta vacio, agregamos las categorias base
            categorias_base = [
                {'id': '1', 'nombre': 'Lácteos'},
                {'id': '2', 'nombre': 'Carnes'},
                {'id': '3', 'nombre': 'Verduras'},
                {'id': '4', 'nombre': 'Bebidas'},
            ]
            for categoria in categorias_base:
                self.categoria_db.agregar(categoria)

    def obtener_todas(self):
        return self.categoria_db.leer_todos() #leemos todas las categorias del archivo CSV y las retornamos
    def obtener_nombre_por_id(self, id):
        categorias = self.obtener_todas() #obtenemos todas las categorias
        for categoria in categorias:
            if categoria['id'] == str(id): #buscamos la categoria que coincida con el ID dado
                return categoria['nombre'] #si encontramos la categoria, retornamos su nombre
        return None #si no encontramos una categoria que coincida, retornamos None