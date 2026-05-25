import re

def validate_required_email(email):
    if not email:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": "Email requerido"
        }

    return {"ok": True}


def validate_email_format(email):
    email_regex = r"^[^@]+@[^@]+\.[^@]+$"

    if not re.match(email_regex, email):
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": "Formato de email inválido"
        }

    return {"ok": True}

def validate_required_password(password, field):
    if not password:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": f"{field} requerida"
        }

    return {"ok": True}


def validate_password_length(password):
    if len(password) < 8:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": "La contraseña debe tener al menos 8 caracteres"
        }

    return {"ok": True}

def validate_password_uppercase(password):
    if not re.search(r"[A-Z]", password):
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": "La contraseña debe tener al menos una letra mayúscula"
        }

    return {"ok": True}


def validate_password_symbol(password):
    if not re.search(r"[^A-Za-z0-9]", password):
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": "La contraseña debe tener al menos un símbolo"
        }

    return {"ok": True}


def validate_password_confirmation(new_password, confirm_password):
    if new_password != confirm_password:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": "La confirmación de contraseña no coincide"
        }

    return {"ok": True}


def validate_login_data(data):
    if not data:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": "Body requerido"
        }

    email = data.get("correo")
    password = data.get("contraseña")

    validation = validate_required_email(email)
    if not validation["ok"]:
        return validation

    validation = validate_email_format(email)
    if not validation["ok"]:
        return validation

    validation = validate_required_password(password, "contraseña")
    if not validation["ok"]:
        return validation

    return {"ok": True}

def validate_change_password_data(data):
    if not data:
        return {
            "ok": False,
            "code": 400,
            "message": "Bad Request",
            "description": "Body requerido"
        }

    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    validation = validate_required_password(current_password, "Contraseña actual")
    if not validation["ok"]:
        return validation

    validation = validate_required_password(new_password, "Nueva contraseña")
    if not validation["ok"]:
        return validation

    validation = validate_required_password(confirm_password, "Confirmación de contraseña")
    if not validation["ok"]:
        return validation

    validation = validate_password_length(new_password)
    if not validation["ok"]:
        return validation

    validation = validate_password_uppercase(new_password)
    if not validation["ok"]:
        return validation

    validation = validate_password_symbol(new_password)
    if not validation["ok"]:
        return validation

    validation = validate_password_confirmation(new_password, confirm_password)
    if not validation["ok"]:
        return validation

    return {"ok": True}


#def validate_register_password(password):
#    validations = [
#        validate_required_password(password),
#        validate_password_length(password),
#        validate_password_uppercase(password),
#        validate_password_symbol(password)
#    ]

#    for validation in validations:
#        if not validation["ok"]:
#            return validation

#    return {"ok": True}

#def validate_register_data(data):
#    if not data:
#        return {
#            "ok": False,
#            "code": 400,
#            "message": "Bad Request",
#            "description": "Body requerido"
#        }

#    password = data.get("password")

#    password_validation = validate_register_password(password)
#    if not password_validation["ok"]:
#        return password_validation
