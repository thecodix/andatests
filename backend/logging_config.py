"""Configuración centralizada de logging para el backend.

Formato de texto plano (nivel + timestamp + logger + mensaje) a stdout, que
Render ya captura y muestra en sus logs de despliegue — no hay servicio
externo de captura de errores (Sentry, etc.) configurado por ahora.
"""
import logging


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
