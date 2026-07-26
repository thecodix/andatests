"""Tests for the rate limiting configured in backend/rate_limit.py and applied
to the sensitive auth endpoints in backend/routers/auth.py."""


def _register(client, email="rate@example.com", password="unaClaveSegura1",
               pregunta="¿Nombre de tu primera mascota?", respuesta="Firulais"):
    return client.post("/api/auth/register", json={
        "email": email,
        "nombre": "Rate",
        "password": password,
        "pregunta_seguridad": pregunta,
        "respuesta_seguridad": respuesta,
    })


def test_login_se_bloquea_pasado_el_limite(client):
    _register(client, email="login_limit@example.com")
    body = {"email": "login_limit@example.com", "password": "incorrecta"}

    for _ in range(5):
        res = client.post("/api/auth/login", json=body)
        assert res.status_code == 401

    res = client.post("/api/auth/login", json=body)
    assert res.status_code == 429


def test_register_se_bloquea_pasado_el_limite(client):
    for i in range(10):
        res = _register(client, email=f"reg{i}@example.com")
        assert res.status_code == 201

    res = _register(client, email="reg_extra@example.com")
    assert res.status_code == 429


def test_reset_password_pregunta_se_bloquea_pasado_el_limite(client):
    _register(client, email="reset_limit@example.com")

    for _ in range(5):
        res = client.post("/api/auth/reset-password/pregunta", json={"email": "reset_limit@example.com"})
        assert res.status_code == 200

    res = client.post("/api/auth/reset-password/pregunta", json={"email": "reset_limit@example.com"})
    assert res.status_code == 429


def test_reset_password_se_bloquea_pasado_el_limite(client):
    _register(client, email="reset2_limit@example.com")
    body = {
        "email": "reset2_limit@example.com",
        "respuesta_seguridad": "incorrecta",
        "nueva_password": "otraClave123",
    }

    for _ in range(5):
        res = client.post("/api/auth/reset-password", json=body)
        assert res.status_code == 401

    res = client.post("/api/auth/reset-password", json=body)
    assert res.status_code == 429
