"""Limiter compartido para las rutas sensibles (login/registro/reset).

Se define en un módulo aparte (en vez de en `main.py`) para que los routers
puedan importarlo sin crear un import circular con la app principal.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
