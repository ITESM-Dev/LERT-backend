from flask_principal import *

admin_permission = Permission(RoleNeed('Admin'))
opManager_permission = Permission(RoleNeed('OpManager'))
manager_permission = Permission(RoleNeed('Manager'))
icaAdmin_permission = Permission(RoleNeed('IcaAdmin'))
manager_or_IcaAdmin = Permission(RoleNeed('Manager'), RoleNeed('IcaAdmin'))

