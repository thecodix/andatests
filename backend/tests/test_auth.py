"""Tests for backend/routers/auth.py — registration, login, and the two-step
security-question password reset flow (replaces the old fixed-password reset)."""


def _register(client, email="ana@example.com", password="unaClaveSegura1",
               pregunta="¿Nombre de tu primera mascota?", respuesta="Firulais"):
    return client.post("/api/auth/register", json={
        "email": email,
        "nombre": "Ana",
        "password": password,
        "pregunta_seguridad": pregunta,
        "respuesta_seguridad": respuesta,
    })


def test_register_requires_security_question(client):
    res = client.post("/api/auth/register", json={
        "email": "sin_pregunta@example.com",
        "nombre": "Ana",
        "password": "unaClaveSegura1",
        "pregunta_seguridad": "",
        "respuesta_seguridad": "",
    })
    assert res.status_code == 422


def test_register_rechaza_contrasena_demasiado_corta(client):
    res = _register(client, email="corta@example.com", password="abc1234")
    assert res.status_code == 422


def test_register_acepta_contrasena_de_longitud_minima(client):
    res = _register(client, email="minima@example.com", password="abcd1234")
    assert res.status_code == 201


def test_register_and_login(client):
    res = _register(client)
    assert res.status_code == 201
    assert res.json()["access_token"]

    res = client.post("/api/auth/login", json={"email": "ana@example.com", "password": "unaClaveSegura1"})
    assert res.status_code == 200
    assert res.json()["access_token"]


def test_reset_password_pregunta_desconocida_da_404(client):
    res = client.post("/api/auth/reset-password/pregunta", json={"email": "no_existe@example.com"})
    assert res.status_code == 404


def test_reset_password_pregunta_devuelve_la_pregunta_configurada(client):
    _register(client)
    res = client.post("/api/auth/reset-password/pregunta", json={"email": "ana@example.com"})
    assert res.status_code == 200
    assert res.json()["pregunta_seguridad"] == "¿Nombre de tu primera mascota?"


def test_reset_password_con_respuesta_incorrecta_falla_y_no_cambia_la_contrasena(client):
    _register(client)
    res = client.post("/api/auth/reset-password", json={
        "email": "ana@example.com",
        "respuesta_seguridad": "respuesta incorrecta",
        "nueva_password": "otraClaveNueva1",
    })
    assert res.status_code == 401

    # La contraseña original sigue funcionando: el intento fallido no la tocó.
    res = client.post("/api/auth/login", json={"email": "ana@example.com", "password": "unaClaveSegura1"})
    assert res.status_code == 200


def test_reset_password_con_respuesta_correcta_cambia_la_contrasena(client):
    _register(client)
    res = client.post("/api/auth/reset-password", json={
        "email": "ana@example.com",
        "respuesta_seguridad": "Firulais",
        "nueva_password": "otraClaveNueva1",
    })
    assert res.status_code == 200
    assert res.json()["access_token"]

    # La contraseña nueva funciona...
    res = client.post("/api/auth/login", json={"email": "ana@example.com", "password": "otraClaveNueva1"})
    assert res.status_code == 200
    # ...y la antigua ya no.
    res = client.post("/api/auth/login", json={"email": "ana@example.com", "password": "unaClaveSegura1"})
    assert res.status_code == 401


def test_reset_password_respuesta_normaliza_mayusculas_y_espacios(client):
    _register(client)
    res = client.post("/api/auth/reset-password", json={
        "email": "ana@example.com",
        "respuesta_seguridad": "  FIRULAIS  ",
        "nueva_password": "otraClaveNueva1",
    })
    assert res.status_code == 200


def test_reset_password_rechaza_contrasena_nueva_demasiado_corta(client):
    _register(client)
    res = client.post("/api/auth/reset-password", json={
        "email": "ana@example.com",
        "respuesta_seguridad": "Firulais",
        "nueva_password": "corta",
    })
    assert res.status_code == 422


def test_set_security_question_para_usuario_ya_autenticado(client):
    token = _register(client).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = client.put("/api/auth/security-question", json={
        "pregunta_seguridad": "¿Ciudad donde naciste?",
        "respuesta_seguridad": "Huelva",
    }, headers=headers)
    assert res.status_code == 200

    res = client.post("/api/auth/reset-password/pregunta", json={"email": "ana@example.com"})
    assert res.status_code == 200
    assert res.json()["pregunta_seguridad"] == "¿Ciudad donde naciste?"
