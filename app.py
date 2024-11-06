from online_storage import FirebaseAuth 
import local_storage
from ui import (
    mostrar_menu_principal, 
    mostrar_dentro_de_la_app,
    mostrar_menu_chats,
    mostrar_menu_amigos,
    mostrar_menu_configuracion
)

firebase_auth = FirebaseAuth()

def inicio():
    iniciar_sesion_automaticamente() #primero intentar iniciar sesion con la local storage
    opcion = mostrar_menu_principal()
    if opcion == "1":
        crear_cuenta()
    elif opcion == "2":
        iniciar_sesion()
    elif opcion == "3":
        salir_app()
    else:
        print("Opción no válida, intenta de nuevo.")
        input("Presiona Enter para continuar...")
        inicio()

def crear_cuenta():
    print("Ingrese los datos para crear su cuenta:")
    username = input("Nombre de Usuario: ")
    password = input("Contraseña: ")
    confirm_password = input("Confirme la Contraseña: ")

    if password != confirm_password:
        print("Las contraseñas no coinciden. Inténtalo de nuevo.")
        input("Presiona Enter para continuar...")
        return crear_cuenta()

    if firebase_auth.crear_usuario(username, password):
        print("Cuenta creada con éxito.")
    input("Presiona Enter para volver al menú principal...")
    inicio()

def iniciar_sesion_automaticamente():
    credenciales = local_storage.cargar_credenciales()

    if credenciales is not None:
        print("Iniciando sesión con credenciales guardadas...")
        username = credenciales["username"]
        password = credenciales["password"]

        if firebase_auth.iniciar_sesion(username, password):
            print("Sesión iniciada correctamente.")
            dentro_de_la_app()
        else:
            print("Error al iniciar sesión con las credenciales guardadas.")
            input("Presiona Enter para ingresar nuevas credenciales...")

def iniciar_sesion():
    print("Ingrese sus credenciales para iniciar sesión:")
    username = input("Nombre de Usuario: ")
    password = input("Contraseña: ")

    if firebase_auth.iniciar_sesion(username, password):
        print("Sesión iniciada correctamente.")
        local_storage.guardar_credenciales(username, password)
        dentro_de_la_app()
    else:
        print("Error al iniciar sesión. Verifique sus credenciales.")
        input("Presiona Enter para continuar...")
        inicio() 

def salir_app():
    print("Fin de la aplicación")
    exit() 

def dentro_de_la_app():
    opcion = mostrar_dentro_de_la_app()
    if opcion == "1":
        chats()
    elif opcion == "2":
        Online()
    elif opcion == "3":
        configuracion()
    elif opcion == "4":
        salir_app()
    else:
        print("Opción no válida, intenta de nuevo.")
        input("Presiona Enter para continuar...")
        dentro_de_la_app()

def chats():
    while True:
        opcion = mostrar_menu_chats()
        if opcion == "1":
            ver_chats()
        elif opcion == "2":
            crear_nuevo_chat()
        elif opcion == "3":
            dentro_de_la_app()
            break
        else:
            print("Opción no válida, intenta de nuevo.")
            input("Presiona Enter para continuar...")

def ver_chats():
    print("Muestra todos los chats con amigos")
    input("Presiona Enter para volver al menú de Chats...")

def crear_nuevo_chat():
    print("Opción para crear un chat con amigos")
    input("Presiona Enter para volver al menú de Chats...")

def Online():
    while True:
        opcion = mostrar_menu_amigos()
        if opcion == "1":
            buscar_usuario()
        elif opcion == "2":
            ver_amigos()
        elif opcion == "3":
            solicitudes_de_amistad()
        elif opcion == "4":
            dentro_de_la_app()
            break
        else:
            print("Opción no válida, intenta de nuevo.")
            input("Presiona Enter para continuar...")

def buscar_usuario():
    print("Escribe el nombre de un usuario")
    input("Presiona Enter para volver al menú de Amigos...")

def ver_amigos():
    print("Muestra la lista de amigos")
    input("Presiona Enter para volver al menú de Amigos...")

def solicitudes_de_amistad():
    print("Muestra las solicitudes recibidas")
    input("Presiona Enter para volver al menú de Amigos...")

def configuracion():
    while True:
        opcion = mostrar_menu_configuracion()
        if opcion == "1":
            cerrar_sesion()
        elif opcion == "2":
            dentro_de_la_app()
            break
        else:
            print("Opción no válida, intenta de nuevo.")
            input("Presiona Enter para continuar...")

def cerrar_sesion():
    local_storage.eliminar_credenciales()
    print("Sesion cerrada, volviendo a inicio...")
    inicio()
