# Backlog priorizado — agente `reparador`

Lista ordenada por prioridad (arriba = primero). El agente `reparador` resuelve **un ítem por invocación**, empezando siempre por el primero que no esté `[x]` hecho. No reordenar manualmente salvo decisión explícita.

---

## 1. Reset de contraseña sin verificación de identidad (account takeover)
**Estado:** [x] hecho
**Área:** seguridad
**Contexto:** `backend/routers/auth.py`, endpoint `POST /auth/reset-password`. Resetea la contraseña de cualquier email existente a un valor fijo y público (`"test1234"`) sin exigir ninguna prueba de que quien llama es el dueño de esa cuenta (ni token por email, ni pregunta de seguridad). Cualquiera que conozca o adivine el email de otro usuario puede tomar el control total de su cuenta en dos peticiones HTTP.
**Criterio de aceptación:** el reseteo de contraseña exige alguna prueba de posesión del email (token de un solo uso con expiración corta enviado por correo, o al menos un flujo de dos pasos) antes de cambiar la contraseña. Si no hay proveedor de email configurado todavía, preguntar al usuario cómo prefiere resolverlo (posponer con un aviso claro, usar un proveedor concreto, u otro mecanismo transitorio) antes de implementar nada.
**Resuelto:** 2026-07-26 — sustituido el reseteo a contraseña fija por un flujo de dos pasos con pregunta de seguridad (elegida por el usuario en el registro): `POST /auth/reset-password/pregunta` devuelve la pregunta configurada, `POST /auth/reset-password` exige la respuesta correcta + una nueva contraseña (mín. 8 caracteres) elegida por el usuario. Nuevo endpoint `PUT /auth/security-question` para que cuentas ya existentes (creadas antes de este cambio, sin pregunta configurada) puedan configurarla una vez logueadas. Añadidas columnas nullable `pregunta_seguridad`/`respuesta_seguridad_hash` a `Usuario` con una migración Alembic real (`a1c8f3d2e9b4`) verificada tanto contra una BD nueva vacía como contra una tabla `usuario` ya existente con datos. Frontend actualizado: registro pide pregunta+respuesta, y "he olvidado mi contraseña" ahora es un flujo de dos pasos en vez del antiguo botón de un clic. Nota: las cuentas preexistentes sin pregunta configurada no podrán auto-recuperar su contraseña hasta usar `PUT /auth/security-question` (no hay UI de ajustes todavía para eso — queda como posible futuro ítem, no bloquea este).
**Tests:** sí — `backend/tests/test_auth.py` (9 tests): registro exige pregunta/respuesta, login, pregunta desconocida da 404, pregunta configurada se devuelve correctamente, respuesta incorrecta falla sin tocar la contraseña, respuesta correcta cambia la contraseña (antigua deja de funcionar), normalización de mayúsculas/espacios en la respuesta, contraseña nueva demasiado corta se rechaza, y `PUT /auth/security-question` para cuentas ya autenticadas. Toda la suite (`uv run python -m pytest`) pasa (9 passed). Se creó la infraestructura de tests de `backend/` desde cero (`pytest` como dev-dependency, `backend/tests/conftest.py` con un engine SQLite temporal compartido para toda la sesión de test, nunca `backend/andatest.db`).

## 2. Rate limiting en endpoints de autenticación
**Estado:** [x] hecho
**Área:** seguridad
**Contexto:** `backend/routers/auth.py` — `/auth/login`, `/auth/register` y `/auth/reset-password` no tienen ningún límite de intentos, lo que permite fuerza bruta de contraseñas y abuso del endpoint de registro/reset.
**Criterio de aceptación:** los tres endpoints tienen un límite razonable de peticiones por IP/tiempo (p.ej. vía `slowapi` u otra librería ligera compatible con FastAPI), devolviendo 429 al superarlo.
**Resuelto:** 2026-07-26 — añadido `slowapi` (dependencia nueva en `backend/pyproject.toml`) con un `Limiter` compartido en `backend/rate_limit.py` (en memoria del proceso, sin Redis — suficiente para el despliegue actual de una sola instancia en Render) y registrado en `main.py` (`app.state.limiter`, exception handler de `RateLimitExceeded` → 429, `SlowAPIMiddleware`). Límites aplicados con `@limiter.limit(...)` por IP a los cuatro endpoints de `backend/routers/auth.py` que forman la superficie de ataque no autenticada del flujo de auth (creció respecto al texto original del ítem tras el ítem 1): `/auth/login` (5/min), `/auth/register` (10/hora), `/auth/reset-password/pregunta` (5/min) y `/auth/reset-password` (5/min). `PUT /auth/security-question` se dejó fuera del alcance por requerir ya autenticación (superficie de ataque mucho menor). Umbrales y ausencia de Redis decididos con el usuario antes de implementar.
**Tests:** sí — `backend/tests/test_rate_limit.py` (4 tests nuevos): cada endpoint devuelve 429 al superar su límite tras agotar las peticiones permitidas dentro de la ventana. Se añadió un fixture `autouse` en `backend/tests/conftest.py` que resetea el `Limiter` (`limiter.reset()`) antes/después de cada test para que los contadores en memoria no se contaminen entre tests. Suite completa (`uv run python -m pytest`, vía `python -m pytest`): 13 passed (9 de antes + 4 nuevos).

## 3. Política mínima de contraseñas en registro
**Estado:** [x] hecho
**Área:** seguridad
**Contexto:** `backend/routers/auth.py`, `RegisterIn.password` no tiene validación de longitud/complejidad mínima — acepta contraseñas triviales o vacías.
**Criterio de aceptación:** `register` rechaza contraseñas por debajo de una longitud mínima razonable (p.ej. 8 caracteres) con un 422 claro.
**Resuelto:** 2026-07-26 — añadido un `field_validator` a `RegisterIn.password` en `backend/routers/auth.py` que exige mínimo 8 caracteres (misma convención ya usada en `ResetPasswordIn.nueva_password` desde el ítem 1), devolviendo 422 si no se cumple. No requirió preguntar nada al usuario: el umbral ya estaba establecido como precedente en el propio código.
**Tests:** sí — `backend/tests/test_auth.py`: `test_register_rechaza_contrasena_demasiado_corta` (7 caracteres → 422) y `test_register_acepta_contrasena_de_longitud_minima` (8 caracteres → 201). Suite completa: 15 passed (13 de antes + 2 nuevos).

## 4. Enumeración de usuarios vía mensajes de error
**Estado:** [x] hecho
**Área:** seguridad
**Contexto:** `backend/routers/auth.py` — `reset-password` devuelve 404 "No existe ningún usuario con ese email", y `register` devuelve 409 "Email ya registrado". Ambos permiten a un atacante confirmar qué emails están registrados en el sistema.
**Criterio de aceptación:** las respuestas no revelan si el email existe o no (mensaje genérico + mismo status/tiempo de respuesta aproximado en los casos que lo permitan sin romper la UX del formulario). Evaluar caso por caso: en `register` puede ser aceptable mantener el aviso (es una decisión de producto habitual), pero `reset-password` debería ser neutro. Si hay dudas de producto, preguntar antes de decidir.
**Resuelto:** 2026-07-26 — al re-analizar el contexto, `reset-password/pregunta` y `reset-password` ya devuelven el mismo mensaje genérico (`SIN_PREGUNTA_SEGURIDAD`, 404) tanto si el email no existe como si existe pero no tiene pregunta de seguridad configurada — esto quedó resuelto como efecto colateral del ítem 1, sin necesitar cambios adicionales de código. Se preguntó al usuario sobre el 409 "Email ya registrado" de `register`: decidió mantenerlo tal cual (patrón de UX estándar, decisión de producto explícita), así que no se tocó.
**Tests:** sí — nuevo test `test_reset_password_pregunta_no_distingue_email_inexistente_de_cuenta_sin_pregunta` en `backend/tests/test_auth.py`: crea una cuenta "legado" sin pregunta de seguridad directamente en BD (simulando una cuenta previa al ítem 1) y confirma que `reset-password/pregunta` devuelve exactamente el mismo status (404) y mensaje que un email que no existe en absoluto. Suite completa: 16 passed (15 de antes + 1 nuevo).

## 5. Migraciones Alembic reales (sustituir el `upgrade()` no-op)
**Estado:** [x] hecho
**Área:** fiabilidad
**Contexto:** `backend/alembic/` tiene versiones placeholder que no hacen nada; el esquema se sincroniza vía `SQLModel.metadata.create_all()` en cada arranque, que solo puede AÑADIR tablas nuevas, nunca alterar columnas existentes (ya obligó a borrar tablas a mano al cambiar `Tarjeta`/`TarjetaEstado`, ver memoria de repo). En producción con usuarios reales esto es peligroso para el próximo cambio de esquema.
**Criterio de aceptación:** al menos la migración inicial genera el esquema real desde los modelos actuales (`alembic revision --autogenerate` o equivalente), y queda documentado el flujo a seguir para futuros cambios de esquema (nueva migración autogenerada + revisión manual, en vez de `create_all` a ciegas).
**Resuelto:** 2026-07-26 — regenerado `backend/alembic/versions/839629e4d06a_initial_schema.py` con `alembic revision --autogenerate` a partir de los modelos actuales de `models.py` (las 10 tablas reales, con todas sus columnas/índices/FKs actuales), sustituyendo el `upgrade()`/`downgrade()` no-op original. Añadido un guard con `sa.inspect()` (igual que en `a1c8f3d2e9b4`): si `tema` ya existe se salta la creación por completo, para no romper despliegues existentes que arrancaron con `create_all()` antes de que esta migración real existiera (sin esa guarda, `alembic upgrade head` fallaría con "table already exists" contra cualquier BD ya poblada sin historial de alembic — verificado el fallo y el arreglo con una BD de prueba simulando ese escenario exacto). Verificado también contra una BD nueva vacía: crea las 10 tablas correctamente y el historial `839629e4d06a → a1c8f3d2e9b4` se aplica sin errores. Documentado el flujo a seguir para futuros cambios de esquema en una nueva sección "Migraciones de base de datos (Alembic)" en `CLAUDE.md`.
**Tests:** sí — `backend/tests/test_migrations.py` (nuevo): ejecuta `alembic upgrade head` (vía subprocess, con su propio proceso Python para no interferir con el `engine`/`DATABASE_URL` ya cacheados por el resto de la suite) contra una BD SQLite limpia y comprueba que las 10 tablas esperadas existen y que `usuario` tiene las columnas de pregunta de seguridad. Suite completa: 17 passed (16 de antes + 1 nuevo).

## 6. CI básica (GitHub Actions) ejecutando la suite de tests
**Estado:** [x] hecho
**Área:** testing
**Contexto:** no existe ningún workflow de CI; los tests que vaya añadiendo `reparador` (y futuros) solo se ejecutan si alguien se acuerda de correrlos a mano.
**Criterio de aceptación:** un workflow en `.github/workflows/` que instale dependencias de `backend/` con `uv` y ejecute `pytest` en cada push/PR.
**Resuelto:** 2026-07-26 — creado `.github/workflows/backend-tests.yml`: en cada push/PR a `master`, instala `uv` (acción oficial `astral-sh/setup-uv`), ejecuta `uv sync --all-groups` (incluye el grupo `dev` con `pytest`) y `uv run pytest -v` sobre `backend/`, en `ubuntu-latest`. Verificado localmente que `uv sync --all-groups` funciona; `uv run pytest` en sí no se pudo verificar literalmente en local por el problema conocido de Windows/antivirus (`Acceso denegado, os error 5`, ver `CLAUDE.md`/memoria de repo — específico de este entorno Windows, no ocurre en runners Linux de GitHub Actions), pero se verificó de forma equivalente con `uv run python -m pytest` (17 passed) para confirmar que la suite y las dependencias están correctas.
**Tests:** N/A (esto ES la infraestructura de tests) — se verificó localmente la suite completa antes de dar el workflow por bueno; la validación definitiva de que el workflow en sí funciona ocurrirá en el primer push/PR a GitHub.

## 7. Logging estructurado y captura de errores en backend
**Estado:** [ ] pendiente
**Área:** operación
**Contexto:** el backend no tiene logging estructurado ni captura de excepciones no controladas (p.ej. fallos de la API de Groq en el asistente, errores 500 en producción) — hoy solo se detectan si un usuario avisa.
**Criterio de aceptación:** logging básico configurado (nivel/formato coherente) y un hook opcional de captura de errores (p.ej. Sentry, activable solo si hay DSN configurado por variable de entorno, sin romper nada si no la hay).
**Tests:** parcial — test de que la app arranca igual con y sin la variable de entorno del proveedor de errores configurada.

## 8. PWA: manifest + service worker básico
**Estado:** [ ] pendiente
**Área:** producto
**Contexto:** `Tests Oposición.dc.html` no tiene `manifest.json` ni service worker — no es instalable como app y no cachea nada para uso offline, pese a ser una app pensada para estudiar en el móvil en ratos sueltos.
**Criterio de aceptación:** manifest válido (icono, nombre, colores) + service worker que cachee al menos los assets estáticos y, si es viable sin complicar demasiado, el banco de preguntas ya descargado para el tema activo.
**Tests:** no aplica de forma significativa (es frontend estático) — validar manualmente que la app se puede instalar y que carga con la red desactivada tras la primera visita.

## 9. Backups automatizados de la base de datos de producción
**Estado:** [ ] pendiente
**Área:** operación
**Contexto:** no hay ninguna estrategia documentada de backup para la base de datos de producción (Postgres/Neon vía Render) — es un punto único de fallo para el progreso de todos los usuarios.
**Criterio de aceptación:** backups automáticos configurados (si el proveedor los ofrece nativamente, documentar cómo activarlos; si no, un script/cron mínimo) y documentado en `CLAUDE.md`/memoria de repo cómo restaurar desde uno.
**Tests:** no aplica (es configuración de infraestructura, no código) — este ítem probablemente requiera preguntar al usuario qué proveedor/plan tiene antes de tocar nada.

## 10. Accesibilidad básica del frontend (ARIA, contraste, foco)
**Estado:** [ ] pendiente
**Área:** producto
**Contexto:** no se ha revisado accesibilidad en `Tests Oposición.dc.html` (labels ARIA, orden de foco por teclado, contraste de color en textos secundarios).
**Criterio de aceptación:** una pasada dirigida (no exhaustiva) que corrija los problemas más evidentes: labels en controles interactivos sin texto visible, contraste mínimo AA en textos, navegación por teclado en el modo test.
**Tests:** no aplica de forma significativa (frontend visual) — validar manualmente con el checklist de accesibilidad básico.

---

## Candidatos sin priorizar todavía (no tocar sin promoverlos antes a un ítem numerado arriba)
- Recordatorios/notificaciones para mantener la racha de estudio.
- Modo oscuro.
- Revisar con `tema-validator` los temas sin informe de validación reciente en `informes/`.
- Ampliar contenido de preguntas reales de los temas 16/17 (hoy muy escaso) si aparecen exámenes nuevos.
