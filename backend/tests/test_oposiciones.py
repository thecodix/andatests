"""Tests para el soporte multi-oposición: listado público, añadir/marcar
favorita en la cuenta de un usuario, y el filtrado de /api/temas."""
from sqlmodel import Session

from database import engine
from models import Oposicion, Tema


def _register(client, email="ana@example.com", password="unaClaveSegura1",
               pregunta="¿Nombre de tu primera mascota?", respuesta="Firulais", oposicion_id=None):
    body = {
        "email": email,
        "nombre": "Ana",
        "password": password,
        "pregunta_seguridad": pregunta,
        "respuesta_seguridad": respuesta,
    }
    if oposicion_id is not None:
        body["oposicion_id"] = oposicion_id
    return client.post("/api/auth/register", json=body)


def _auth_headers(client, **kwargs):
    token = _register(client, **kwargs).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _crear_segunda_oposicion():
    """La oposición 1 ya la seedea el fixture `client`; para los tests que
    necesitan una segunda, se inserta directamente (equivalente a lo que hará
    `seed.py` cuando exista contenido real para ella)."""
    with Session(engine) as s:
        s.add(Oposicion(id=1001, slug="oposicion-2", nombre="Segunda oposición de prueba"))
        s.add(Tema(id=1001, titulo="Tema 1 de la oposición 2", ley="Ley Z", orden=0, oposicion_id=1001))
        s.commit()


def test_listado_publico_de_oposiciones_no_requiere_autenticacion(client):
    res = client.get("/api/oposiciones")
    assert res.status_code == 200
    slugs = {o["slug"] for o in res.json()}
    assert "aux-admin-c2-uhu" in slugs


def test_registro_anade_la_oposicion_por_defecto_como_favorita(client):
    headers = _auth_headers(client)
    res = client.get("/api/me/oposiciones", headers=headers)
    assert res.status_code == 200
    mis = res.json()
    assert len(mis) == 1
    assert mis[0]["id"] == 1
    assert mis[0]["favorita"] is True


def test_anadir_segunda_oposicion_no_es_favorita_por_defecto(client):
    _crear_segunda_oposicion()
    headers = _auth_headers(client)

    res = client.post("/api/me/oposiciones", json={"oposicion_id": 1001}, headers=headers)
    assert res.status_code == 201
    mis = {o["id"]: o for o in res.json()}
    assert mis[1]["favorita"] is True
    assert mis[1001]["favorita"] is False


def test_anadir_oposicion_ya_anadida_da_409(client):
    headers = _auth_headers(client)
    res = client.post("/api/me/oposiciones", json={"oposicion_id": 1}, headers=headers)
    assert res.status_code == 409


def test_anadir_oposicion_inexistente_da_404(client):
    headers = _auth_headers(client)
    res = client.post("/api/me/oposiciones", json={"oposicion_id": 999}, headers=headers)
    assert res.status_code == 404


def test_marcar_favorita_cambia_cual_se_carga_por_defecto(client):
    _crear_segunda_oposicion()
    headers = _auth_headers(client)
    client.post("/api/me/oposiciones", json={"oposicion_id": 1001}, headers=headers)

    res = client.put("/api/me/oposiciones/1001/favorita", headers=headers)
    assert res.status_code == 200
    mis = {o["id"]: o for o in res.json()}
    assert mis[1001]["favorita"] is True
    assert mis[1]["favorita"] is False

    res = client.get("/api/temas", headers=headers)
    assert res.status_code == 200
    temas = res.json()
    assert len(temas) == 1
    assert temas[0]["id"] == 1001


def test_marcar_favorita_de_oposicion_no_anadida_da_404(client):
    _crear_segunda_oposicion()
    headers = _auth_headers(client)
    res = client.put("/api/me/oposiciones/1001/favorita", headers=headers)
    assert res.status_code == 404


def test_temas_filtra_por_oposicion_favorita_por_defecto(client):
    _crear_segunda_oposicion()
    headers = _auth_headers(client)

    res = client.get("/api/temas", headers=headers)
    assert res.status_code == 200
    ids = {t["id"] for t in res.json()}
    assert 1001 not in ids  # el usuario todavía no ha añadido esa oposición


def test_temas_con_oposicion_id_explicito_no_anadida_da_403(client):
    _crear_segunda_oposicion()
    headers = _auth_headers(client)
    res = client.get("/api/temas", params={"oposicion_id": 1001}, headers=headers)
    assert res.status_code == 403


def test_temas_con_oposicion_id_explicito_anadida_funciona(client):
    _crear_segunda_oposicion()
    headers = _auth_headers(client)
    client.post("/api/me/oposiciones", json={"oposicion_id": 1001}, headers=headers)

    res = client.get("/api/temas", params={"oposicion_id": 1001}, headers=headers)
    assert res.status_code == 200
    ids = {t["id"] for t in res.json()}
    assert ids == {1001}
