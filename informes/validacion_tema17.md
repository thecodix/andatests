# Validación Tema 17 — Microsoft 365: Excel

Fuente de verdad: `.cache/tema17_temario_tema17.txt` (temario oficial, 8 págs, leído completo).
Banco: `banco/tema17.json` — 168 preguntas.

Resumen: 2 ERR corregidas · 6 WARN · 2 REVIEW · resto OK (158).

## Errores corregidos (ERR)

```
ERR | "vista que muestra la disposición ... como se imprimirá" | Excel 365 - Vistas
    | Temario: "la vista que representa la hoja como se imprimirá se denomina en Excel Diseño de página"
    | y "«Diseño de impresión» de Word". c corregido 2 -> 1 (Diseño de página). El propio exp lo marcaba
    | para revisar; ademas coincide con otras 2 preguntas del banco que ya dan "Diseño de página".

ERR | "atajo de teclado para crear un libro en blanco" | Excel 365 - Atajos de teclado
    | Temario: "Crear un libro ... El atajo de teclado es CTRL+U". Clave del examen (test_80) tambien = C (CTRL+U).
    | c corregido 3 (CTRL+N) -> 2 (CTRL+U). exp actualizado.
```

## Advertencias (WARN — no modificadas)

```
WARN | "¿qué opción es correcta para guardar un archivo?" | Excel 365 - Guardar
     | Temario: la barra de acceso rápido "incluye comandos como Guardar". Tanto CTRL+G (op.1, clave) como
     | "herramienta de guardar de la barra de acceso rápido" (op.2) son válidas -> dos respuestas correctas.
WARN | "atajo para acceder a Formato de Celda" (CTRL+MAY+F) | Excel 365 - Atajos de teclado
     | Temario: "se abre con CTRL+1 (o CTRL+MAY+F ...)". El atajo habitual (CTRL+1) no está entre las opciones;
     | CTRL+MAY+F es válido segun temario, c=1 se sostiene. exp ya lo aclara.
WARN | "¿existe la opción de bloquear celdas?" (B y C correctas) | Excel 365 - Proteger celdas
     | Temario: bloqueo via Formato de celdas (pestaña Proteger) surte efecto al proteger la hoja. Opción B cita
     | "grupo alineación" (impreciso: es el iniciador de diálogo de ese grupo). Respuesta agregada aceptable.
WARN | "opción FILTRO, ¿en qué pestaña?" (Inicio) | Excel 365 - Filtro
     | Temario ubica Filtrar en Datos y en Inicio > Buscar y seleccionar/Ordenar y filtrar. Op. correcta (Inicio)
     | válida; Datos también lo tendría, pero no figura como opción.
WARN | "para abrir un libro existente" (pestaña inicio, CTRL+A) | Excel 365 - Abrir libro
     | Temario: "Abrir un libro existente: Archivo > Abrir ... El atajo es CTRL+A". El atajo es correcto; la
     | ubicación "pestaña inicio" es imprecisa (es Archivo). exp ya lo señala.
WARN | "etiquetas de las hojas" (sin color y se ven en blanco) | Excel 365 - Etiquetas de hoja
     | Temario: "las etiquetas no tienen color asignado (fondo blanco y texto en negro)". Redacción de opciones
     | 1/2 confusa (color de fondo vs. de texto), pero la elegida es la coherente.
```

## A revisar (REVIEW — no modificadas)

```
REVIEW | "abrir desde el icono de Excel, ¿qué acción no se podrá realizar?" (activar pestaña archivo)
       | El temario no describe la pantalla de inicio con ese detalle; no se puede confirmar contra el temario.
REVIEW | "¿qué pestaña activar para llegar a la opción Documento en blanco?" (ninguna correcta)
       | Depende del matiz "Documento en blanco" (término de Word; en Excel es "Libro en blanco"). El temario no
       | lo plantea así explícitamente; la clave del examen da "ninguna", se respeta.
```

## OK (evidencia representativa)

- Libro/extensión: Temario "El archivo que crea ... se denomina libro" / ".xlsx" / "una sola hoja" — coincide.
- Atajos: Temario anexo confirma ALT+F4 (cerrar Excel), CTRL+F4 (cerrar libro), CTRL+G (guardar), MAY+F11
  (insertar hoja), MAY+F3 (insertar función), ALT+F1/F11 (gráfico), CTRL+INICIO (A1), CTRL+MAY+Espacio (toda
  la hoja), CTRL+INTRO (rango), CTRL+F1 (contraer cinta), CTRL+rueda (zoom) — todas coinciden.
- Referencias: Temario "$A10 es mixta con la columna fija; A$10 es mixta con la fila fija" y "$A$1 fija columna
  y fila" — coincide con todas las preguntas de referencias.
- Funciones: Temario "ABS ... valor absoluto", "RESIDUO ... resto de una división", "PROMEDIO ... estadística",
  "AHORA() ... fecha y hora", "SI ... lógica", "TRUNCAR/ENTERO matemáticas; LARGO de texto" — coincide.
- Operadores: Temario clasifica & (concatenación), : (referencia/rango), <> (distinto), = (comparación) — coincide.
- Errores: Temario tabla #####, #¡REF!, #¿NOMBRE? — coincide.
- Vistas/impresión/formato/protección/formato condicional/datos/gráficos: verificado contra sec. 6-12 del temario.

Estado JSON: válido, 168 preguntas, campos {q,o,c,ref,exp} intactos. banco.js regenerado (2565 preguntas, 17 temas).
