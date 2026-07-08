# Validación Tema 17 — Microsoft 365: Excel

Fuente de verdad: `pdfs/tema17/temario/tema17.pdf` (síntesis propia de temario-generator; cacheado en `.cache/tema17_temario_tema17.txt`).
Fuentes secundarias (claves oficiales): exámenes Test 80, 82, 83, 113, 117, 120.
Banco: `banco/tema17.json` — 163 preguntas.

Resumen: 155 OK · 6 ERR (corregidas) · 2 WARN · 0 REVIEW.

## Erratas corregidas (ERR)

```
ERR    | q_022 | Vistas Excel        | Temario: "la vista que representa la hoja como se imprimirá se denomina en Excel Diseño de página" — c de 2 (Diseño de impresión) a 1 (Diseño de página)
ERR    | q_034 | Atajo nuevo libro   | Temario: "El atajo de teclado es CTRL+U"; clave Test 80 Q4 = C (CTRL+U) — c de 3 (CTRL+N) a 2 (CTRL+U)
ERR    | q_089 | Sintaxis función    | Enunciado decía "fórmula" (con =A5+B5 también válido); restaurado a "función" para que =SUMA sea la única correcta. Temario: "=SUMA(A1:A4)"
ERR    | q_102 | Biblioteca funciones| Enunciado decía "Biblioteca de funciones" con respuesta "No existe" (falso). Restaurado a "Biblioteca de fórmulas" (grupo inexistente). Temario: "El grupo Biblioteca de funciones se encuentra en la pestaña Fórmulas"
ERR    | q_147 | Formato condicional | Temario: "no existe la opción «compartir regla»" y "Administrar reglas" sí existe — c de 2 (Administrar reglas) a 1 (Compartir regla)
ERR    | q_148 | Formato condicional | Temario: "Conjuntos de iconos (por ejemplo, iconos direccionales)" y "las reglas se aplican a celdas, no «a libros»" — c de 0 (Resaltar reglas de libros) a 2 (Conjunto de iconos direccionales)
```

## Puntos débiles (WARN, no modificados)

```
WARN   | q_030 | Test 80 Q1          | "Documento en blanco": clave oficial marca D (Ninguna de las anteriores) pese a que la ruta pasa por Archivo>Nuevo; enunciado con opciones ambiguas. Se respeta clave oficial.
WARN   | q_155 | Formato de celdas   | Test 83 Q19: tanto CTRL+1 como CTRL+MAY+F abren Formato de celdas (temario los da ambos). El banco fija CTRL+1; la clave del examen marcaba CTRL+MAY+F. Ambas válidas.
```

## Notas sobre preguntas señaladas por el generador

- Test 117 Q4 (q_022): resuelto como ERR → "Diseño de página" (coincide con la pregunta hermana q_142 del mismo banco).
- Test 82 Q15 (q_102): "Biblioteca de fórmulas" no existe → "No existe" es correcta tras restaurar el enunciado.
- Test 82 Q42 (q_138): "Comprobación de errores busca errores... (pestaña Fórmulas)" → solo A correcta (c=0). Confirmado OK.
- Test 82 Q43 (q_139): Filtro; entre las opciones dadas (sin "Datos"), Inicio es la correcta. OK.
- Test 82 Q5 (q_089): resuelto como ERR de enunciado ("fórmula"→"función").
- Test 82 Q34 (q_130): "proteger un libro" — Revisar no figura entre las opciones; entre las dadas, Archivo es correcta (temario: Archivo>Información>Proteger libro). OK.
- Test 83 Q23 / Q23BIS (q_147 / q_148): ambas corregidas contra el temario (ver ERR).
- Test 80 Q28 (q_047): temario "Buscar y reemplazar (atajos CTRL+B... CTRL+L)"; CTRL+C es copiar → "No se puede usar el atajo CTRL+C" es cierta (c=2). Confirmado OK.

## Verificación por bloques (OK) — muestras de evidencia del temario

- Entorno/pantalla (q_001–q_021, q_035–q_072): "celdas, que constituyen la unidad básica"; "Libro1 - Excel"; "cuadro de nombres... referencia de la celda activa"; "no existe ninguna «barra de cálculo»". Coinciden.
- Libros/hojas/celdas (q_073–q_088, q_090–q_101): "El archivo... se denomina libro"; ".xlsx"; "una sola hoja"; "máximo de 31 caracteres y no puede contener \\ / ? * [ ] :"; "MAY+F11... a la izquierda de la hoja activa". Coinciden.
- Desplazamiento/edición (q_103–q_128): "Celda de arriba... MAY+INTRO"; "INICIO... primera celda de la fila activa"; "(10) se interpreta como –10"; "ESC... cancela"; "SUPR borra el contenido... conserva el formato". Coinciden.
- Fórmulas/funciones/referencias (q_015–q_018, q_129–q_170): "Toda fórmula comienza... por el signo ="; "& (une cadenas)"; "ABS... valor absoluto"; "RESIDUO... resto"; "=(A1+B2)*C3"; "$A$1... no varía al copiarla"; "A$10 es mixta con la fila fija". Coinciden.
- Gráficos/datos (q_113–q_115, q_133–q_140): "grupo Gráficos... pestaña Insertar"; "ALT+F1... incrustado"; "F11... hoja de gráfico independiente"; "«pentagrama» no es un tipo de gráfico"; "Quitar duplicados... Herramientas de datos". Coinciden.
- Formato/protección/impresión (q_141–q_163): "no existe la opción «combinar verticalmente»"; "General... sin formato numérico específico"; "Código postal... Especial"; "celdas... bloqueadas"; "Proteger libro... estructura"; "Área de impresión... no incluye las celdas vacías"; "CTRL+P... vista previa e impresión". Coinciden.

Todas las demás preguntas no listadas como ERR/WARN se han contrastado con el pasaje correspondiente del temario y son OK.
