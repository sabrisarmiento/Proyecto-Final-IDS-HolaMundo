from helpers.constants import NIVEL_AYUDANTE, NIVEL_PROFESOR, NIVEL_SUPERADMIN

def can_manage_admin_level(nivel_logged_user, nivel_target):
    can_manage = False

    if nivel_logged_user == NIVEL_SUPERADMIN:
        can_manage = nivel_target in [NIVEL_PROFESOR, NIVEL_AYUDANTE]

    elif nivel_logged_user == NIVEL_PROFESOR:
        can_manage = nivel_target == NIVEL_AYUDANTE

    return can_manage
