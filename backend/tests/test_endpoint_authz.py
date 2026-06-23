from helpers import user_belongs


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_user_can_manage_course_superadmin_skips_query(monkeypatch):
    called = {"q": False}

    def fake_query(*a, **k):
        called["q"] = True
        return []

    monkeypatch.setattr(user_belongs, "query_db", fake_query)
    assert user_belongs.user_can_manage_course(1, {"nivel": 3, "id_usuario": 99}) is True
    assert called["q"] is False


def test_user_can_manage_course_owner(monkeypatch):
    monkeypatch.setattr(user_belongs, "query_db", lambda *a, **k: [{"id_profesor": 7}])
    assert user_belongs.user_can_manage_course(1, {"nivel": 2, "id_usuario": 7}) is True


def test_user_can_manage_course_not_owner(monkeypatch):
    monkeypatch.setattr(user_belongs, "query_db", lambda *a, **k: [{"id_profesor": 7}])
    assert user_belongs.user_can_manage_course(1, {"nivel": 2, "id_usuario": 8}) is False


def test_user_can_manage_course_missing_course(monkeypatch):
    monkeypatch.setattr(user_belongs, "query_db", lambda *a, **k: [])
    assert user_belongs.user_can_manage_course(1, {"nivel": 2, "id_usuario": 7}) is False


def test_courses_mutations_reject_unauthenticated(client):
    assert client.post("/courses", json={}).status_code == 401
    assert client.patch("/courses/1", json={}).status_code == 401


def test_courses_mutations_reject_ayudante(client, make_token):
    token = make_token(1)
    assert client.post("/courses", json={}, headers=auth_header(token)).status_code == 403
    assert client.patch("/courses/1", json={}, headers=auth_header(token)).status_code == 403


def test_patch_course_non_owner_forbidden(client, make_token, monkeypatch):
    monkeypatch.setattr("controllers.courses_controller.user_can_manage_course", lambda id_course, user: False, raising=False)
    token = make_token(2)
    assert client.patch("/courses/1", json={"catedra": "X"}, headers=auth_header(token)).status_code == 403


def test_promocion_reject_unauthenticated(client):
    assert client.post("/cursos/1/promocion", json={}).status_code == 401


def test_promocion_reject_ayudante(client, make_token):
    token = make_token(1)
    assert client.post("/cursos/1/promocion", json={}, headers=auth_header(token)).status_code == 403


def test_promocion_non_owner_forbidden(client, make_token, monkeypatch):
    monkeypatch.setattr("services.exam_service.user_can_manage_course", lambda id_course, user: False, raising=False)
    token = make_token(2)
    assert client.post("/cursos/1/promocion", json={"es_promocionable": True}, headers=auth_header(token)).status_code == 403


def test_clases_mutations_reject_unauthenticated(client):
    assert client.post("/clases", json={}).status_code == 401
    assert client.patch("/clases/1", json={}).status_code == 401
    assert client.delete("/clases/1").status_code == 401


def test_clases_mutations_reject_ayudante(client, make_token):
    token = make_token(1)
    assert client.post("/clases", json={}, headers=auth_header(token)).status_code == 403
    assert client.patch("/clases/1", json={}, headers=auth_header(token)).status_code == 403
    assert client.delete("/clases/1", headers=auth_header(token)).status_code == 403


def test_clases_non_owner_forbidden(client, make_token, monkeypatch):
    monkeypatch.setattr("services.class_service.user_can_manage_course", lambda id_course, user: False, raising=False)
    monkeypatch.setattr("services.class_service.user_can_manage_clase", lambda id_clase, user: False, raising=False)
    token = make_token(2)
    assert client.post("/clases", json={"id_curso": 1}, headers=auth_header(token)).status_code == 403
    assert client.patch("/clases/1", json={"temas": "X"}, headers=auth_header(token)).status_code == 403
    assert client.delete("/clases/1", headers=auth_header(token)).status_code == 403


def test_enviar_link_reject_unauthenticated(client):
    assert client.post("/asistencia/enviar-link", json={}).status_code == 401


def test_enviar_link_reject_ayudante(client, make_token):
    token = make_token(1)
    assert client.post("/asistencia/enviar-link", json={"id_clase": 1}, headers=auth_header(token)).status_code == 403


def test_enviar_link_non_owner_forbidden(client, make_token, monkeypatch):
    monkeypatch.setattr("services.attendance_service.user_can_manage_clase", lambda id_clase, user: False, raising=False)
    token = make_token(2)
    assert client.post("/asistencia/enviar-link", json={"id_clase": 1}, headers=auth_header(token)).status_code == 403


def test_students_mutations_reject_unauthenticated(client):
    assert client.post("/students", json={}).status_code == 401
    assert client.post("/students/import").status_code == 401
    assert client.patch("/students/1", json={}).status_code == 401


def test_students_mutations_reject_ayudante(client, make_token):
    token = make_token(1)
    assert client.post("/students", json={"id_curso": 1}, headers=auth_header(token)).status_code == 403
    assert client.post("/students/import", headers=auth_header(token)).status_code == 403
    assert client.patch("/students/1", json={}, headers=auth_header(token)).status_code == 403


def test_students_non_owner_forbidden(client, make_token, monkeypatch):
    monkeypatch.setattr("services.student_service.user_can_manage_course", lambda id_course, user: False, raising=False)
    monkeypatch.setattr("services.student_service.user_can_manage_alumno", lambda id_alumno, user: False, raising=False)
    token = make_token(2)
    assert client.post("/students", json={"id_curso": 1}, headers=auth_header(token)).status_code == 403
    assert client.patch("/students/1", json={"nombre": "X"}, headers=auth_header(token)).status_code == 403


def test_equipo_alumno_reject_unauthenticated(client):
    assert client.post("/equipo-alumno", json={}).status_code == 401
    assert client.delete("/equipo-alumno", json={}).status_code == 401


def test_equipo_alumno_reject_ayudante(client, make_token):
    token = make_token(1)
    assert client.post("/equipo-alumno", json={"id_equipo": 1}, headers=auth_header(token)).status_code == 403
    assert client.delete("/equipo-alumno", json={"id_equipo": 1}, headers=auth_header(token)).status_code == 403


def test_equipo_alumno_non_owner_forbidden(client, make_token, monkeypatch):
    monkeypatch.setattr("services.team_student_service.user_can_manage_equipo", lambda id_equipo, user: False, raising=False)
    token = make_token(2)
    assert client.post("/equipo-alumno", json={"id_equipo": 1}, headers=auth_header(token)).status_code == 403
    assert client.delete("/equipo-alumno", json={"id_equipo": 1}, headers=auth_header(token)).status_code == 403
