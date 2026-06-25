# Handoff: Andatest — App de Tests de Oposición (PAS · Universidad de Huelva)

## Overview
Andatest es una aplicación web de **autoevaluación tipo test** para preparar la oposición de acceso a la **Escala Auxiliar Administrativa (C2) de la Universidad de Huelva**. Cubre 17 temas, con tests por tema / aleatorios / simulacro / repaso de falladas, corrección con explicación legal (artículo citado), estadísticas por tema, evolución temporal, racha de estudio, predicción de nota, falladas y ranking/logros.

El objetivo de este handoff es **llevar el prototipo (hoy 100% frontend con persistencia en localStorage) a una arquitectura real**: backend **FastAPI**, base de datos mínima (**SQLite** en desarrollo → **PostgreSQL** en producción), y despliegue en cloud (**Railway / Render / Fly.io**). El usuario seguirá editando el contenido a partir de los JSON por tema ya existentes.

## About the Design Files
Los archivos de este paquete son **referencias de diseño creadas en HTML** — un prototipo funcional que muestra el aspecto y el comportamiento esperados, **no código de producción para copiar tal cual**. El frontend está construido como un único componente (`Tests Oposición.dc.html`) con un runtime propio (`support.js`). 

La tarea es **doble**:
1. **Backend nuevo (FastAPI)**: implementar la API y la base de datos descritas más abajo. El banco de preguntas (`banco/temaN.json`) sirve como *seed* directo.
2. **Frontend**: puede recrearse en el entorno del cliente (React/Vue/...) **o** reutilizar el HTML actual sustituyendo la capa de persistencia `localStorage` por llamadas `fetch` a la API. La lógica y el modelo de datos ya coinciden, así que el refactor es acotado.

## Fidelity
**Alta fidelidad (hifi)** en el frontend: colores, tipografía, espaciado e interacciones son definitivos. La parte de backend es una **especificación** a implementar, no código existente.

---

## Modelo de datos (entidades)

> Diseño pensado para SQLModel (Pydantic + SQLAlchemy). Las estadísticas NO se almacenan: se **derivan** por consulta sobre `respuesta`. Esto reproduce exactamente lo que el frontend calcula hoy en memoria.

### `tema`
| campo | tipo | notas |
|---|---|---|
| id | int PK | 1..17 |
| titulo | str | p.ej. "La Constitución Española de 1978" |
| ley | str | p.ej. "CE 1978" |
| orden | int | para ordenar en la UI |

### `pregunta`
| campo | tipo | notas |
|---|---|---|
| id | str PK | estable, formato `"{tema}_{indice}"` (p.ej. `"1_0"`) — **clave**: las falladas y el progreso dependen de este id estable |
| tema_id | int FK → tema.id | |
| enunciado | str | (`q` en el JSON) |
| opciones | JSON list[str] | exactamente 4 (`o` en el JSON) |
| correcta | int | índice 0..3 de la opción correcta (`c`) |
| ref | str | artículo de ley citado (p.ej. "Art. 1.2 CE") |
| explicacion | str | (`exp`) |

### `usuario`
| campo | tipo | notas |
|---|---|---|
| id | int PK | |
| email | str unique | |
| nombre | str | |
| hashed_password | str | si se añade auth (fase posterior) |
| created_at | datetime | |

### `sesion` (un test completado)
| campo | tipo | notas |
|---|---|---|
| id | int PK | |
| usuario_id | int FK | |
| modo | enum | `tema` \| `aleatorio` \| `simulacro` \| `falladas` |
| tema_id | int FK nullable | solo en modo `tema` |
| feedback | enum | `inmediato` \| `final` |
| total | int | nº de preguntas |
| aciertos | int | |
| segundos | int nullable | duración (modo simulacro) |
| created_at | datetime | usado para racha, evolución y "sesiones este mes" |

### `respuesta` (una pregunta respondida dentro de una sesión)
| campo | tipo | notas |
|---|---|---|
| id | int PK | |
| sesion_id | int FK | |
| pregunta_id | str FK | |
| elegida | int nullable | índice 0..3, null = sin responder |
| correcta | bool | conveniencia (== pregunta.correcta) |

**Falladas**: se derivan → preguntas cuya última respuesta del usuario fue incorrecta (o `COUNT(incorrectas) - COUNT(correctas) > 0`, que es como lo cuenta el prototipo). Recomendado: vista/consulta que devuelva, por usuario, las preguntas con saldo de fallos > 0 y su nº de veces.

---

## Contrato de API (REST, FastAPI)

> Prefijo sugerido `/api`. Auth opcional al principio (un único usuario demo); cuando se añada, proteger con JWT Bearer.

### Contenido (lectura)
- `GET /api/temas` → `[{id, titulo, ley, orden, total_preguntas}]`
- `GET /api/temas/{tema_id}/preguntas` → `[{id, enunciado, opciones[], ref, ...}]`
  - ⚠️ **Seguridad anti-trampa (opcional)**: en modo `final`/simulacro se puede omitir `correcta` y `explicacion` en la respuesta y validarlos en el servidor al enviar. En el prototipo actual se envía todo al cliente (es estudio personal, aceptable).
- `GET /api/preguntas/aleatorias?n=10&temas=1,2,3` → muestreo aleatorio
- `GET /api/falladas` → preguntas falladas del usuario `[{...pregunta, veces}]`

### Tests (escritura)
- `POST /api/sesiones` → crea una sesión con sus respuestas. Body:
  ```json
  {
    "modo": "tema",
    "tema_id": 1,
    "feedback": "inmediato",
    "segundos": 312,
    "respuestas": [
      { "pregunta_id": "1_0", "elegida": 1 },
      { "pregunta_id": "1_3", "elegida": null }
    ]
  }
  ```
  El servidor calcula `correcta` por respuesta, `aciertos`/`total`, persiste y actualiza la racha. Devuelve `{ sesion_id, aciertos, total, pct, nota }`.

### Estadísticas (derivadas)
- `GET /api/stats/resumen` → `{ acierto_global, total_hechas, total_preguntas, prediccion, num_falladas, racha, mejor_racha, total_sesiones, temas_flojos }`
- `GET /api/stats/por-tema` → `[{ tema_id, intentos, aciertos, pct, seen }]`
- `GET /api/stats/evolucion?limit=10` → `[pct, pct, ...]` (últimas N sesiones, para la gráfica)
- `GET /api/stats/calendario?dias=35` → `["2026-06-01", ...]` (días con sesión, para el heatmap de racha)
- `GET /api/ranking/semanal` → `[{ nombre, puntos, es_yo }]` (puntos = aciertos*10 + sesiones*20 en el prototipo; ajustar)

### Lógica de negocio a replicar (ya implementada en el frontend, ver `Tests Oposición.dc.html`)
- **Predicción de nota** = `acierto_global / 100 * 10`, con un decimal.
- **Racha**: +1 si la última sesión fue ayer; =1 si hay un hueco; sin cambio si ya se estudió hoy. `mejor_racha = max(racha histórica)`.
- **% por tema** = `aciertos_tema / intentos_tema * 100`.
- **Temas flojos** = nº de temas con intentos>0 y pct<55.
- **Logros** (derivables): primer test, racha≥7, 100% en un test, ≥80% en 5 temas, ≥100 preguntas respondidas, 0 falladas con ≥1 sesión.

---

## Pila tecnológica recomendada (por pasos)

### 1. Contenido editable
Mantener `banco/temaN.json` (un archivo por tema, formato `{q, o, c, ref, exp}`). Editar = tocar el JSON. Es el **seed** de la BD. Incluido en este paquete: carpeta `banco/`.

### 2. Backend (FastAPI + SQLModel)
```
fastapi, uvicorn[standard], sqlmodel, alembic, pydantic-settings
# auth (fase posterior): python-jose[cryptography], passlib[bcrypt]
```
- `SQLModel` para definir entidades una sola vez.
- `Alembic` para migraciones desde el día 1.
- Script `seed.py` que lee `banco/temaN.json` + metadatos de temas y puebla `tema` y `pregunta` (ver `seed_reference.py` incluido).

### 3. Base de datos
- **SQLite** en local (`sqlite:///./andatest.db`) — cero setup.
- **PostgreSQL** en producción. Con SQLModel, cambiar solo `DATABASE_URL`.

### 4. Conexión del frontend
Sustituir en el frontend la lectura/escritura de `localStorage` (clave `andatest_progress_v2`) por `fetch` a la API; mantener localStorage como **caché offline**. El banco se carga de `GET /api/temas/...` en vez de `banco.js`.

### 5. Deploy
- **Railway** o **Render**: deploy desde git, Postgres gestionado, mínima config. **Fly.io** si se quiere Docker.
- **Dockerfile** (python:3.12-slim + uvicorn). El frontend estático puede ir en el mismo servicio o en Cloudflare Pages/Vercel/Netlify.
- Variables: `DATABASE_URL`, `SECRET_KEY` (si hay auth), `CORS_ORIGINS`.

---

## Design tokens (frontend hifi)
- **Acento (violeta)**: `#6B46E5` · oscuro `#5333C4` · fondo suave `#F4F1FE` · borde `#E6DEFB`
- **Semánticos**: correcto `#2E9E6B` · error `#D6455B` · aviso `#E0922F`
- **Neutros**: texto `#1B1B22` · texto sec. `#6B6B78` · gris `#9A9AA6` · borde `#ECECF1` · fondo página `#F7F7FA` · tarjeta `#FFFFFF`
- **Tipografía**: títulos **Newsreader** (serif, 500/600); cuerpo **Libre Franklin** (400–700)
- **Radios**: tarjetas 14–18px · botones 11–13px · chips 7–8px
- **Sombra hover tarjeta**: `0 8px 24px rgba(27,27,34,.08)`
- **Escala**: páginas con `max-width:1080px`; sidebar 248px

## Pantallas (resumen)
1. **Inicio/Dashboard** — 3 variantes conmutables (Resumen / Foco / Datos): KPIs, progreso por bloques, predicción de nota, accesos a modos de test.
2. **Temas** — lista de los 17 temas con % de acierto y progreso.
3. **Setup de test** — elegir modo de corrección (inmediato/final) y nº de preguntas.
4. **Test** — pregunta + 4 opciones; feedback verde/rojo; explicación + artículo; cronómetro en simulacro.
5. **Resultados** — anillo de acierto, nota, revisión pregunta a pregunta.
6. **Estadísticas** — KPIs, gráfica de evolución (SVG), heatmap de racha, detalle por tema, botón reiniciar progreso.
7. **Falladas** — lista de preguntas pendientes con su respuesta correcta y explicación.
8. **Ranking y logros** — clasificación semanal e insignias desbloqueables.

Responsive: sidebar fija en escritorio; barra de navegación inferior en móvil (`max-width:820px`).

## Files (incluidos en este paquete)
- `Tests Oposición.dc.html` — prototipo completo (referencia de UI + lógica de negocio a portar).
- `support.js` — runtime del componente (solo si se reutiliza el HTML tal cual).
- `banco.js` — banco ensamblado que consume el frontend (auto-generado).
- `banco/temaN.json` — **fuente de la verdad** del contenido (455 preguntas, 17 archivos). Seed de la BD.
- `seed_reference.py` — script de referencia para poblar la BD desde los JSON.

## Notas
- El progreso vive hoy en el navegador (localStorage, clave `andatest_progress_v2`), por lo que es individual del equipo. La migración a backend lo centraliza por usuario.
- **Revisar el contenido legal**: las preguntas fueron generadas a partir del temario PDF y están ancladas a artículos reales, pero conviene validarlas antes de un uso serio (especialmente las respuestas correctas y permisos/plazos que cambian con reformas).
- Los temas 16 y 17 tienen pocas preguntas (3 c/u) porque, según el propio temario, tienen carácter abierto y no entran en las pruebas de acceso libre; se mantienen por petición del usuario.
