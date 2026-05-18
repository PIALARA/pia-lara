from flask_principal import Permission, RoleNeed

# Definir permisos
admin_permission = Permission(RoleNeed("admin"))
tecnico_permission = Permission(RoleNeed("tecnico"))
cliente_permission = Permission(RoleNeed("cliente"))

# Definir
admin_o_tecnico = Permission(RoleNeed("admin"), RoleNeed("tecnico"))
