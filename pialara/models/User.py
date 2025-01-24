from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, mail, nombre, password, rol, activo, ultima_conexion, parent="",font_size=1.0):
        self.id = id
        self.email = mail
        self.nombre = nombre
        self.password = password
        self.rol = rol
        self.activo=activo
        self.ultima_conexion = ultima_conexion
        self.parent = parent
        self.font_size = font_size

    def __str__(self):
        return f"{self.email} ({self.nombre} / {self.password})"
