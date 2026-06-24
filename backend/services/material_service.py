from helpers.responses import error_response, success_response
from helpers.user_belongs import user_can_manage_course, user_can_manage_material
from controllers.materials_controller import get_all_materials, create_material, delete_material_by_id, update_material

def materials_service(filters):
    result = get_all_materials(filters)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "materials": result["data"]
    })

def create_material_service(data, user):
    if not user_can_manage_course((data or {}).get("id_curso"), user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este curso"
        })
    result = create_material(data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    }, 201)

def delete_material_service(id_material, user):
    if not user_can_manage_material(id_material, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este material"
        })
    result = delete_material_by_id(id_material)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })

def update_material_service(id_material, data, user):
    if not user_can_manage_material(id_material, user):
        return error_response({
            "ok": False, "code": 403,
            "message": "Forbidden", "description": "No tenés permisos sobre este material"
        })
    result = update_material(id_material, data)
    if not result["ok"]:
        return error_response(result)
    return success_response({
        "message": result["message"]
    })
