from flask_login import UserMixin

class UserStats(UserMixin):
    def __init__(self, id, mail, nombre, password, rol, ultima_conexion, parent="", fecha_nacimiento=None, sexo=None, provincia=None, enfermedades=None, dis=None, cant_audios=None,audios_mes=None, font_size=1.0):
        self.id = id
        self.email = mail
        self.nombre = nombre
        self.password = password
        self.rol = rol
        self.ultima_conexion = ultima_conexion
        self.parent = parent
        self.font_size = font_size
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.provincia = provincia
        self.enfermedades = enfermedades if enfermedades else []
        self.dis = dis if dis else []
        self.cant_audios = cant_audios if cant_audios else 0
        self.audios_mes=audios_mes

    def __str__(self):
        return f"{self.user['mail']} ({self.user['nombre']} / {self.user['password']})"
