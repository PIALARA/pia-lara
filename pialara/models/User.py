from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, mail, nombre, password, rol, ultima_conexion, parent=""):
        self.id = id
        self.email = mail
        self.nombre = nombre
        self.password = password
        self.rol = rol
        self.ultima_conexion = ultima_conexion
        self.parent = parent

    def __str__(self):
        return f"{self.email} ({self.nombre} / {self.password})"
