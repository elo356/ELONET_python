from firebase import FirebaseAuth 
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
    """Verifica y muestra los chats donde el usuario está participando."""
    username = local_storage.cargar_credenciales()["username"]
    chats_participados = firebase_auth.ver_chats(username)  

    if chats_participados:
        print("Chats disponibles en los que estás participando:")
        chats_con_participacion = []  
        for index, chat in enumerate(chats_participados, 1):
   
            if username in chat['participants']:
                chats_con_participacion.append(chat)
                print(f"{index}. Chat ID: {chat['chat_id']}, Nombre: {chat['chat_name']}, Participantes: {chat['participants']}")

        if not chats_con_participacion:
            print("No estás participando en ningún chat.")
            input("Presiona Enter para volver al menú de Chats...")
            return  

        chat_opcion = int(input("\nSelecciona el número del chat al que deseas entrar (o escribe 0 para volver): "))
        if chat_opcion == 0:
            return 

        elif 1 <= chat_opcion <= len(chats_con_participacion):
            chat = chats_con_participacion[chat_opcion - 1]
            print(f"Entrando al chat {chat['chat_name']}...")

            while True:
                accion = input(f"\n¿Qué deseas hacer en el chat {chat['chat_name']}?\n"
                               "1. Abandonar el chat\n"
                               "2. Eliminar el chat\n"
                               "3. Volver a los chats\n"
                               "4. Entrar a este chat\n"
                               "Selecciona una opción: ")

                if accion == "1":
                    print(f"Abandonando el chat {chat['chat_name']}...")
                    firebase_auth.abandonar_chat(username, chat['chat_id'])
                    break  
                elif accion == "2":
                    confirmacion = input(f"¿Estás seguro de que deseas eliminar el chat {chat['chat_name']}? (s/n): ").lower()
                    if confirmacion == "s":
                        firebase_auth.eliminar_chat(username, chat['chat_id'])
                    break  
                elif accion == "3":
                    break 
                elif accion == "4":
                    cargar_chat(chat)
                else:
                    print("Opción no válida, intenta de nuevo.")
        else:
            print("Opción no válida, intenta de nuevo.")
    else:
        print("No estás participando en ningún chat.")
    
    input("Presiona Enter para volver al menú de Chats...")

def crear_nuevo_chat():
    print("Crear un nuevo chat con amigos.")

    # Obtener lista de amigos del usuario
    username = local_storage.cargar_credenciales()["username"]
    amigos = firebase_auth.obtener_amigos(username)

    if amigos: 
        print("Lista de amigos: ")
        for i, amigo in enumerate(amigos, 1):
            print(f"{i}. {amigo}")

        seleccionados = input("Selecciona los números de amigos para crear el chat (separados por comas): ")
        amigos_seleccionados = [amigos[int(i)-1] for i in seleccionados.split(",")]

        chat_name = input("Ingresa el nombre del chat: ")
        chat_id = firebase_auth.crear_nuevo_chat(username, amigos_seleccionados, chat_name)

        print(f"Chat '{chat_name}' creado exitosamente con ID: {chat_id}")
    else:
        print("No tienes amigos disponibles para crear un chat.")
    
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

def ver_amigos():
    """Muestra la lista de amigos del usuario y permite eliminar un amigo."""
    username = local_storage.cargar_credenciales()["username"]
    amigos = firebase_auth.obtener_amigos(username)
    
    if amigos:
        print("Lista de amigos:")
        for index, amigo in enumerate(amigos, 1):
            print(f"{index}. {amigo}")
    else:
        print("No tienes amigos agregados aún.")
    
    # Menú de opciones
    while True:
        print("\nOpciones:")
        print("1. Eliminar un amigo")
        print("2. Volver")
        opcion = input("Selecciona una opción (1-2): ")

        if opcion == "1":
            eliminar_amigo(amigos, username)
        elif opcion == "2":
            return  
        else:
            print("Opción no válida, intenta de nuevo.")
            input("Presiona Enter para continuar...")

def eliminar_amigo(amigos, username):
    """Elimina un amigo de la lista del usuario."""
    try:
        nombre_amigo = input("Introduce el nombre del amigo que deseas eliminar: ")
        
        # Verificar si el amigo está en la lista de amigos
        if nombre_amigo in amigos:
            # Eliminar al amigo de la lista de amigos en la base de datos
            firebase_auth.eliminar_amigo(username, nombre_amigo)
            print(f"Amigo {nombre_amigo} eliminado correctamente.")
        else:
            print(f"No tienes a {nombre_amigo} en tu lista de amigos.")
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    input("Presiona Enter para continuar...")

def buscar_usuario():
    """Permite buscar un usuario y enviar solicitud de amistad si es encontrado."""
    username = local_storage.cargar_credenciales()["username"]
    usuario_destino = input("Escribe el nombre del usuario que deseas buscar: ")
    if usuario_destino == username:
        print("No puedes buscar ni enviar solicitud a ti mismo.")
    elif firebase_auth.db.child(usuario_destino).get():
        enviar = input(f"{usuario_destino} encontrado. ¿Quieres enviar una solicitud de amistad? (s/n): ").lower()
        if enviar == "s":
            firebase_auth.enviar_solicitud(username, usuario_destino)
        else:
            print("Solicitud no enviada.")
    else:
        print(f"El usuario {usuario_destino} no existe.")
    input("Presiona Enter para volver al menú de Amigos...")

def solicitudes_de_amistad():
    """Permite al usuario gestionar sus solicitudes de amistad: ver, aceptar o rechazar."""
    username = local_storage.cargar_credenciales()["username"]
    solicitudes = firebase_auth.db.child(username).child("solicitudes").get() or []
    
    if not solicitudes:
        print("No tienes solicitudes de amistad pendientes.")
    else:
        print("Solicitudes de amistad recibidas:")
        for amigo in solicitudes:
            print(f"- {amigo}")
        
        while True:
            amigo = input("Escribe el nombre del usuario cuya solicitud quieres gestionar (o escribe 'volver' para regresar): ")
            if amigo == "volver":
                break
            elif amigo in solicitudes:
                accion = input(f"¿Deseas aceptar o rechazar la solicitud de {amigo}? (aceptar/rechazar): ").strip().lower()
                if accion == "aceptar":
                    firebase_auth.aceptar_solicitud(username, amigo)
                elif accion == "rechazar":
                    firebase_auth.rechazar_solicitud(username, amigo)
                else:
                    print("Opción no válida. Intenta de nuevo.")
            else:
                print("No tienes una solicitud pendiente de ese usuario.")
    input("Presiona Enter para volver al menú de Amigos...")

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

def cargar_chat(chat):
    """Muestra un chat y permite enviar mensajes."""
    print(f"Entrando al chat {chat['chat_name']}...")
    chat_id = chat['chat_id']
    
    firebase_auth.obtener_mensajes(chat_id)

    while True:
        mensaje = input(f"Escribe un mensaje en el chat {chat['chat_name']} (o escribe 'salir' para volver): ")
        
        if mensaje.lower() == "salir":
            break
        else:
            sender = local_storage.cargar_credenciales()["username"]
            firebase_auth.enviar_mensaje(chat_id, sender, mensaje)
            firebase_auth.obtener_mensajes(chat_id)  
