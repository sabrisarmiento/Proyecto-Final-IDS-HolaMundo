def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_roles_and_dashboard_reject_unauthenticated(client):
    assert client.post("/roles", json={}).status_code == 401
    assert client.delete("/roles/1").status_code == 401
    assert client.get("/dashboard/general").status_code == 401
    assert client.post("/dashboard/roles", json={}).status_code == 401
    assert client.delete("/dashboard/roles/1").status_code == 401


def test_roles_and_dashboard_reject_non_superadmin(client, make_token):
    for nivel in (1, 2):
        token = make_token(nivel)
        assert client.post("/roles", json={}, headers=auth_header(token)).status_code == 403
        assert client.delete("/roles/1", headers=auth_header(token)).status_code == 403
        assert client.get("/dashboard/general", headers=auth_header(token)).status_code == 403
        assert client.post("/dashboard/roles", json={}, headers=auth_header(token)).status_code == 403
        assert client.delete("/dashboard/roles/1", headers=auth_header(token)).status_code == 403


def test_superadmin_passes_the_level_gate(client, make_token, monkeypatch):
    monkeypatch.setattr("routes.route_roles.create_rol_service", lambda data: ("", 201))
    monkeypatch.setattr("routes.route_roles.delete_rol_service", lambda id: ("", 200))
    monkeypatch.setattr("routes.route_dashboard_general.get_general_dashboard", lambda: {"ok": True, "data": {}})
    monkeypatch.setattr("routes.route_dashboard_general.create_rol", lambda data: {"ok": True, "message": "ok", "id": 1})
    monkeypatch.setattr("routes.route_dashboard_general.delete_rol_by_id", lambda id_rol: {"ok": True})
    token = make_token(3)
    assert client.post("/roles", json={}, headers=auth_header(token)).status_code == 201
    assert client.delete("/roles/1", headers=auth_header(token)).status_code == 200
    assert client.get("/dashboard/general", headers=auth_header(token)).status_code == 200
    assert client.post("/dashboard/roles", json={}, headers=auth_header(token)).status_code == 201
    assert client.delete("/dashboard/roles/1", headers=auth_header(token)).status_code == 200
