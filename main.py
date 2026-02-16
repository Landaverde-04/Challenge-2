from infraestructura.file_manager import FileManager
import os
import time

def menu_principal():
    os.system("cls")  # Limpiar la consola 
    print("Bienvenido al sistema de gestión de usuarios")
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
    return
        

if __name__ == "__main__":
    menu_principal()