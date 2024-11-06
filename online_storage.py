import firebase_admin
from firebase_admin import credentials, db
import local_storage

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