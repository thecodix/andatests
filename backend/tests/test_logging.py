"""Tests para el logging básico y la captura de excepciones no controladas
configurados en backend/main.py + backend/logging_config.py."""
import logging

from fastapi.testclient import TestClient

import main as main_module
from auth import get_current_user


def test_la_app_arranca_y_responde_al_healthcheck(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_excepcion_no_controlada_devuelve_500_generico_y_queda_registrada_en_el_log(client, caplog):
    # raise_server_exceptions=False: queremos comprobar la respuesta HTTP real
    # que recibiría un cliente (gestionada por nuestro exception_handler), no
    # que TestClient vuelva a lanzar la excepción hacia el propio test (su
    # comportamiento por defecto, pensado para depurar en desarrollo).
    def _boom():
        raise RuntimeError("fallo simulado para test de logging")

    main_module.app.dependency_overrides[get_current_user] = _boom
    try:
        with TestClient(main_module.app, raise_server_exceptions=False) as no_raise_client:
            with caplog.at_level(logging.ERROR, logger="andatest"):
                res = no_raise_client.get("/api/auth/me")
        assert res.status_code == 500
        assert res.json() == {"detail": "Error interno del servidor"}
        assert any("Error no controlado" in r.message for r in caplog.records)
    finally:
        main_module.app.dependency_overrides.pop(get_current_user, None)
