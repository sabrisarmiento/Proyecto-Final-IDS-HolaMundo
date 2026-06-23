from helpers.responses import error_response, success_response
from helpers.user_belongs import user_can_manage_course, user_can_manage_clase
from controllers.classes_controller import get_classes, get_class_id, create_class, update_class, delete_class, get_classes_by_subject

def class_service(filters):
    result = get_classes(filters)
    
    if not result["ok"]:
        return error_response(result)

    return success_response({"classes": result["data"]})

def class_get_service(id_clase):
    result = get_class_id(id_clase)
    
    if not result["ok"]:
        return error_response(result)

    return success_response({"class": result["data"]})   

def create_class_service(data, user):
    if not user_can_manage_course(data.get("id_curso"), user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este curso"
        })
    result = create_class(data)
    
    if not result["ok"]:
        return error_response(result)

    return success_response({"message": result["message"]}, 201)

def update_class_service(id_clase, data, user):
    if not user_can_manage_clase(id_clase, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre esta clase"
        })
    result = update_class(id_clase, data)
    
    if not result["ok"]:
        return error_response(result)
        
    return success_response({"message": result["message"]})

def delete_class_service(id_clase, user):
    if not user_can_manage_clase(id_clase, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre esta clase"
        })
    result = delete_class(id_clase)
    
    if not result["ok"]:
        return error_response(result)
        
    return success_response({"message": result["message"]})

def classes_by_subject_service(id_subject):
    result = get_classes_by_subject(id_subject)

    if not result["ok"]:
        return error_response(result)

    return success_response({"classes": result["data"]})