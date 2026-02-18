#Este archivo es el puente por asi decirlo entre la capa de infraestructura y la capa de presentacion, es decir, aqui se hace la logica de negocio para manejar los usuarios, como crear un nuevo usuario, obtener todos los usuarios, etc.

from infraestructura.file_manager import FileManager
from clases.models import Usuario

class UserService:
    def __init__(self):
        columnas_usuario = ['id', 'username', 'password', 'rol', 'nombres', 'apellidos', 'es_primer_ingreso']
        self.usuario_db = FileManager('usuarios.csv', columnas_usuario) #usamos el FileManager para manejar el archivo CSV de usuarios
    
    def crear_usuario(self, nombres, apellidos, password, rol):
        nuevo_id = self.usuario_db.obtener_nuevo_id() #obtenemos el nuevo ID usando el metodo del FileManager
        nuevo_usuario = Usuario(nuevo_id, nombres, apellidos, password, rol) #creamos una instancia de Usuario, el username se genera automaticamente
        self.usuario_db.agregar(nuevo_usuario.to_dict()) #agregamos el nuevo usuario al archivo CSV usando el metodo agregar del FileManager
        return nuevo_usuario.username #retornamos el username del nuevo usuario creado
    
    def autenticar(self, username, password):
        usuarios = self.usuario_db.leer_todos() #leemos todos los usuarios del archivo CSV
        for usuario_dict in usuarios:
            if usuario_dict['username'] == username and usuario_dict['password'] == password:
                return Usuario(
                    id=int(usuario_dict['id']),
                    nombres=usuario_dict['nombres'],
                    apellidos=usuario_dict['apellidos'],
                    password=usuario_dict['password'],
                    rol=usuario_dict['rol'],
                    es_primer_ingreso=usuario_dict['es_primer_ingreso'] == 'True',
                    username=usuario_dict['username']
                )
        return None #si no encontramos un usuario que coincida, retornamos None

    def cambiar_password(self, username, nueva_password):
        usuarios = self.usuario_db.leer_todos() #leemos todos los usuarios del archivo CSV
        usuario_encontrado = False
        for usuario_dict in usuarios:
            if usuario_dict['username'] == username: #buscamos el usuario que coincida con el username dado
                usuario_dict['password'] = nueva_password #si encontramos el usuario, actualizamos su password
                usuario_dict['es_primer_ingreso'] = 'False' #marcamos que ya no es su primer ingreso
                usuario_encontrado = True
                break
        if usuario_encontrado:
           self.usuario_db.guardar_todo(usuarios) #sobrescribimos el archivo CSV con los datos actualizados
           return True #retornamos True para indicar que el cambio de password fue exitoso
        else:
            return False #retornamos False para indicar que el cambio de password no fue exitoso, aunque en este caso no deberia pasar porque ya validamos que el usuario existe 

    def actualizar_datos_usuario(self, username, nuevos_nombres, nuevos_apellidos, nueva_password):
        usuarios = self.usuario_db.leer_todos() #leemos todos los usuarios del archivo CSV
        usuario_encontrado = False
        for usuario_dict in usuarios:
            if usuario_dict['username'] == username: #buscamos el usuario que coincida con el username dado
                if nuevos_nombres:
                    usuario_dict['nombres'] = nuevos_nombres #si se proporcionan nuevos nombres, actualizamos el campo de nombres
                if nuevos_apellidos:
                    usuario_dict['apellidos'] = nuevos_apellidos #si se proporcionan nuevos apellidos, actualizamos el campo de apellidos
                if nueva_password:
                    usuario_dict['password'] = nueva_password #si se proporciona una nueva password, actualizamos el campo de password
                usuario_encontrado = True
                break
        if usuario_encontrado:
           self.usuario_db.guardar_todo(usuarios) #sobrescribimos el archivo CSV con los datos actualizados
           return True #retornamos True para indicar que la actualización de datos fue exitosa
        else:
           raise ValueError("Usuario no encontrado.") #si no encontramos un usuario que coincida, lanzamos una excepción indicando que el usuario no fue encontrado

