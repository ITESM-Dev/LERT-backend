from flask_principal import *

admin_permission = Permission(RoleNeed('Admin'))
opManager_permission = Permission(RoleNeed('OpManager'))
manager_permission = Permission(RoleNeed('Manager'))
icaAdmin_permission = Permission(RoleNeed('IcaAdmin'))
manager_or_IcaAdmin = Permission(RoleNeed('Manager'), RoleNeed('IcaAdmin'))
manager_or_OpManager = Permission(RoleNeed('Manager'), RoleNeed('OpManager'))
manager_or_OpManager_or_icaAdmin = Permission(RoleNeed('Manager'), RoleNeed('OpManager'), RoleNeed('IcaAdmin'))


