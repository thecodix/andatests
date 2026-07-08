# Validación tema 7 — LO 3/2018 Protección de Datos

Fuente: `pdfs/tema7/temario/tema 7_fin.pdf` (arts. 4-18) vs `banco/tema7.json` (87 preguntas).

## Resumen

- Total: 87 preguntas
- OK: 81
- ERR corregidas: 2 (q_17, q_34)
- WARN: 3 (q_04, q_69, q_83)
- REVIEW: 1 (q_48)

## Correcciones aplicadas (ERR)

- **q_17** (TEST 105 nº17, art. 10): clave corregida de C a A. Temario art. 10.1: "amparado en una norma de Derecho de la Unión, en esta ley orgánica o en otras normas de rango legal". La opción A ("una norma de rango legal") es amparo literal válido; la C ("cualquier norma legislativa del Estado Español") es imprecisa. `ref` ajustada a Art. 10.1.
- **q_34** (TEST 105 nº34, art. 16): clave corregida de C a B. Temario art. 16.2: "debe constar claramente en los sistemas de información del responsable" (opción B), no "accesos remotos" (C). `ref` ajustada a Art. 16.2.

## Confirmadas correctas tras revisión (sin cambios)

- **q_04** (TEST 105 nº4, art. 5): clave D correcta. Temario: "así como todas las personas que intervengan en cualquier fase" — ninguna de A/B/C lo recoge bien.
- **q_48** (TEST 60 nº14, art. 10): clave D correcta (REVIEW por diseño, pregunta-trampa). El enunciado usa fines EXCLUIDOS por el art. 10.1 ("para fines distintos de"); para esos fines no procede ninguno de los amparos → D.
- **q_69** (TEST 87 nº10, art. 8.1): clave D (WARN). Enunciado de art. 8.1 con opciones propias del art. 8.2; única opción con "norma con rango de Ley" es D. Redacción poco precisa.
- **q_83** (TEST 87 nº24, art. 15.2): clave A correcta (WARN). Temario: "impedir tratamientos futuros para fines de mercadotecnia directa". Redacción de opción algo ambigua por OCR.
- **q_32** (TEST 60 nº23, art. 14): ya estaba en A, correcto — temario exige documentación "de la inexactitud o carácter incompleto".

## Otros hallazgos (no bloqueantes)

- **q_43** (art. 8.1): el enunciado dice "Según el art. 7" pero contenido y `ref` (Art. 8.1) son de obligación legal — probable mislabel del examen original. Respuesta y clave correctas, no tocado.
- Discrepancias menores de subapartado en `ref` (p.ej. encargado-tramita citado como 12.4 en banco vs 12.3 en temario; prueba de cumplimiento 12.4 vs 12.2). Contenido y clave correctos en todos los casos, no son errores factuales.

## Estado final

87 preguntas, JSON válido (`q/o[4]/c∈0-3/ref/exp`). `banco.js` regenerado (1621 preguntas totales en todo el banco).
