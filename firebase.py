import firebase_admin
from firebase_admin import credentials, db
import local_storage
import uuid
import datetime

cred = credentials.Certificate("elonet-a7e27-firebase-adminsdk-m5hsw-72300bd67e.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://elonet-a7e27-default-rtdb.firebaseio.com/'
})

class FirebaseAuth:
    def __init__(self):
        self.db = db.reference('users') 

    def crear_usuario(self, username, password):
        """Crear una cuenta de usuario con nombre de usuario y contraseña"""
        # Verificar si el usuario ya existe
        if self.db.child(username).get():
            print("El nombre de usuario ya existe.")
            return False
        
        # Crear un nuevo usuario
        self.db.child(username).set({
            'username': username,
            'password': password
        })
        print(f"Cuenta creada exitosamente para {username}.")
        return True

    def iniciar_sesion(self, username, password):
        """Iniciar sesión con nombre de usuario y contraseña"""
        # Buscar el usuario en la base de datos
        user_data = self.db.child(username).get()
        
        if not user_data:
            print("El usuario no existe.")
            return False
        
        # Verificar si la contraseña es correcta
        if user_data['password'] == password:
            print(f"Sesión iniciada correctamente para {username}.")
            
            # Guardar las credenciales localmente
            local_storage.guardar_credenciales(username, password)
            return True
        else:
            print("Contraseña incorrecta.")
            return False
        
    def enviar_solicitud(self, usuario_actual, usuario_destino):
        if usuario_actual == usuario_destino:
            print("No puedes enviarte una solicitud a ti mismo.")
            return
        solicitudes_destino = self.db.child(usuario_destino).child("solicitudes").get() or []
        if usuario_actual in solicitudes_destino:
            print(f"Ya has enviado una solicitud a {usuario_destino}.")
            return
        solicitudes_destino.append(usuario_actual)
        self.db.child(usuario_destino).child("solicitudes").set(solicitudes_destino)
        print(f"Solicitud enviada a {usuario_destino}.")

    def aceptar_solicitud(self, usuario_actual, amigo):
        solicitudes = self.db.child(usuario_actual).child("solicitudes").get() or []
        if amigo not in solicitudes:
            print("No tienes una solicitud pendiente de este usuario.")
            return
        # Eliminar solicitud de la lista
        solicitudes.remove(amigo)
        self.db.child(usuario_actual).child("solicitudes").set(solicitudes)
        # Añadir a la lista de amigos de ambos
        amigos_usuario = self.db.child(usuario_actual).child("amigos").get() or []
        amigos_amigo = self.db.child(amigo).child("amigos").get() or []
        amigos_usuario.append(amigo)
        amigos_amigo.append(usuario_actual)
        self.db.child(usuario_actual).child("amigos").set(amigos_usuario)
        self.db.child(amigo).child("amigos").set(amigos_amigo)
        print(f"Ahora eres amigo de {amigo}.")

    def rechazar_solicitud(self, usuario_actual, amigo):
        solicitudes = self.db.child(usuario_actual).child("solicitudes").get() or []
        if amigo in solicitudes:
            solicitudes.remove(amigo)
            self.db.child(usuario_actual).child("solicitudes").set(solicitudes)
            print(f"Solicitud de {amigo} rechazada.")
        
    def obtener_amigos(self, username):
        """Obtiene la lista de amigos del usuario."""
        amigos = self.db.child(username).child("amigos").get()
        if amigos:
            return amigos
        else:
            return []
        
    def eliminar_amigo(self, username, amigo):
        """Elimina un amigo de la lista del usuario en la base de datos."""
      
        user_ref = self.db.child(username).child("amigos")
        
        amigos = user_ref.get()  
        if amigos and amigo in amigos:
            amigos.remove(amigo)  
            user_ref.set(amigos)  
        else:
            print(f"No se encontró a {amigo} en la lista de amigos de {username}.")

        amigo_ref = self.db.child(amigo).child("amigos")
        amigos_amigo = amigo_ref.get()  
        if amigos_amigo and username in amigos_amigo:
            amigos_amigo.remove(username)  
            amigo_ref.set(amigos_amigo)    
        else:
            print(f"No se encontró a {username} en la lista de amigos de {amigo}.")

    def crear_nuevo_chat(self, user_id, amigos, chat_name):
        """Crea un nuevo chat con los amigos seleccionados y lo guarda en la categoría de chats"""
        chat_id = str(uuid.uuid4())  
        participantes = [user_id] + amigos  
        chats_ref = db.reference('chats')
        chats_ref.child(chat_id).set({
            "chat_name": chat_name,
            "participants": participantes,
            "messages": {}  # Inicialmente no hay mensajes
        })
        print(f"Chat '{chat_name}' creado con éxito.")
        return chat_id  

    def ver_chats(self, user_id):
        """Muestra todos los chats en los que el usuario está participando."""
        try:
            chats_ref = db.reference('chats')  
            chats = chats_ref.get()  

            chats_participados = []
            for chat_id, chat_data in chats.items():
                if user_id in chat_data['participants']:  # Verifica si el userid está en la lista de participantes
                    chats_participados.append({
                        'chat_id': chat_id,
                        'chat_name': chat_data['chat_name'],
                        'participants': chat_data['participants']
                    })
        except:
            print("No tienes chats")
        return chats_participados

    def abandonar_chat(self, user_id, chat_id):
        """Permite al usuario abandonar un chat (ser eliminado de la lista de participantes)."""
        chats_ref = db.reference('chats')
        chat_data = chats_ref.child(chat_id).get()  # Obtener los datos del chat

        if chat_data:
            if user_id in chat_data['participants']:  # Verifica si el usuario está en el chat
                chat_data['participants'].remove(user_id)
                chats_ref.child(chat_id).update({
                    'participants': chat_data['participants']
                })
                print(f"Has abandonado el chat {chat_id}.")
            else:
                print(f"No estás en el chat {chat_id}.")
        else:
            print(f"El chat {chat_id} no existe.")

    def eliminar_chat(self, user_id, chat_id):
        """Elimina un chat si el usuario es participante."""
        chats_ref = db.reference('chats')
        chat_data = chats_ref.child(chat_id).get()  # Obtener datos del chat

        if chat_data:
            if user_id in chat_data['participants']:  # Verifica si el usuario es un participante
                # Eliminar el chat de la base de datos
                chats_ref.child(chat_id).delete()
                print(f"Chat {chat_id} eliminado correctamente.")
            else:
                print("No puedes eliminar este chat porque no eres un participante.")
        else:
            print(f"Chat {chat_id} no encontrado.")

    def enviar_mensaje(self, chat_id, sender, mensaje):
        """Envía un mensaje en el chat especificado."""
        chats_ref = db.reference('chats')
        chat_data = chats_ref.child(chat_id).get()

        if chat_data:
            # Obtener el diccionario de mensajes del chat
            messages = chat_data.get("messages", {})
        
            message_id = str(uuid.uuid4())
        
            # Agregar el mensaje al diccionario de mensajes
            messages[message_id] = {
                'sender': sender,
                'message': mensaje,
                'timestamp': datetime.datetime.now().strftime(("%H:%M:%S"))
            }

         # Actualizar el chat con el nuevo mensaje
            chats_ref.child(chat_id).update({
                'messages': messages
            })
            print(f"Mensaje enviado: {mensaje}")
        else:
            print("El chat no existe.")
            
    def obtener_mensajes(self, chat_id):
        """Obtiene los mensajes de un chat ordenados por timestamp."""
        chats_ref = db.reference('chats')
        chat_data = chats_ref.child(chat_id).get()

        if chat_data:
            # Obtener todos los mensajes
            messages = chat_data.get("messages", {})
        
            # Ordenar los mensajes por timestamp
            sorted_messages = sorted(messages.items(), key=lambda x: x[1]['timestamp'])
        
        # Mostrar los mensajes
            for message_id, message_data in sorted_messages:
                print(f"{message_data['sender']}, {message_data['timestamp']}: {message_data['message']}")
        else:
            print("El chat no existe.")
    def mostrar_chat_en_tiempo_real(self, chat_id):
        """Muestra los mensajes en tiempo real de un chat."""
        chats_ref = db.reference(f'chats/{chat_id}/messages')

        def on_message_added(snapshot):
            message_data = snapshot.val()
            print(f"{message_data['sender']}: {message_data['message']}")

        chats_ref.listen(on_message_added)
