from infraestructura.file_manager import FileManager

columnas_usuario = ['id', 'username', 'password', 'rol', 'nombres', 'apellidos']
usuario_db = FileManager('usuarios.csv', columnas_usuario)

# 2. Generar un ID automático
nuevo_id = usuario_db.obtener_nuevo_id()
print(f"El próximo ID será: {nuevo_id}")

# 3. Guardar un usuario de prueba (simulando Admin)
nuevo_usuario = {
    'id': nuevo_id,
    'username': 'ADMIN2',
    'password': '123',
    'rol': 'Cliente',
    'nombres': 'Jose',
    'apellidos': 'Landaverde'
}

usuario_db.agregar(nuevo_usuario)
print("Usuario guardado.")

# 4. Leer para verificar
todos = usuario_db.leer_todos()
print(todos)