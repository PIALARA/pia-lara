from bson import ObjectId
from flask_login import UserMixin


class User(UserMixin):
    def __init__(
        self,
        id: ObjectId,
        mail: str,
        nombre: str,
        password: str,
        rol: str,
        activo: bool,
        ultima_conexion: str,
        parent: str = "",
        font_size: float = 1.0,
        selected_badge: str | None = None,
    ):
        self.id = id
        self.email = mail
        self.nombre = nombre
        self.password = password
        self.rol = rol
        self.activo = activo
        self.ultima_conexion = ultima_conexion
        self.parent = parent
        self.font_size = font_size
        self.selected_badge = selected_badge

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return f"{self.email} ({self.nombre} / {self.password})"
