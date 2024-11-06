import os
from colorama import Fore, Style, init

init(autoreset=True)

def limpiar_consola():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def encabezado():
    """Muestra el encabezado de la aplicación"""
    print(Fore.CYAN + Style.BRIGHT + "********************************")
    print(Fore.YELLOW + Style.BRIGHT + "            ELONET             ")
    print(Fore.CYAN + Style.BRIGHT + "********************************\n")

def mostrar_menu_principal():
    """Muestra el menú principal"""
    limpiar_consola()
    encabezado()
    print(Fore.GREEN + "Menú Principal")
    print("1. Crear Cuenta")
    print("2. Iniciar Sesión")
    print("3. Salir de la App")
    return input(Fore.LIGHTWHITE_EX + "Selecciona una opción (1-3): ")

def mostrar_dentro_de_la_app():
    """Muestra el menú de opciones dentro de la app"""
    limpiar_consola()
    encabezado()
    print(Fore.GREEN + "Dentro de la App")
    print("1. Chats")
    print("2. Online")
    print("3. Configuración")
    print("4. Salir de la App")
    return input(Fore.LIGHTWHITE_EX + "Selecciona una opción (1-4): ")

def mostrar_menu_chats():
    """Muestra el menú de opciones dentro de Chats"""
    limpiar_consola()
    encabezado()
    print(Fore.GREEN + "Menú de Chats")
    print("1. Ver Chats")
    print("2. Crear Nuevo Chat")
    print("3. Volver")
    return input(Fore.LIGHTWHITE_EX + "Selecciona una opción (1-3): ")

def mostrar_menu_amigos():
    """Muestra el menú de opciones dentro de Amigos"""
    limpiar_consola()
    encabezado()
    print(Fore.GREEN + "Menú Online")
    print("1. Buscar Usuario")
    print("2. Ver Amigos")
    print("3. Solicitudes de Amistad")
    print("4. Volver")
    return input(Fore.LIGHTWHITE_EX + "Selecciona una opción (1-4): ")

def mostrar_menu_configuracion():
    """Muestra el menú de opciones dentro de Configuración"""
    limpiar_consola()
    encabezado()
    print(Fore.GREEN + "Configuración")
    print("1. Logout")
    print("2. Volver")
    return input(Fore.LIGHTWHITE_EX + "Selecciona una opción (1-2): ")