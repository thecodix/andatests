# Validación Tema 17 — Microsoft 365: Excel

**Fecha:** 2026-07-21  
**Fuente de verdad:** `.cache/tema17_temario_tema17.txt` (temario Excel 365, 8 páginas)  
**Banco:** `banco/tema17.json` — 178 preguntas (8 tests: 80, 82, 83, 113, 117, 120, 125, 129)  
**Resultado global:** 173 OK · 2 ERR (corregidas) · 3 WARN · 0 REVIEW

---

## ERR corregidas

ERR       | q_22 (idx 21) | Excel 365 - Vistas               | Temario: "la vista que representa la hoja como se imprimirá se denomina en Excel Diseño de página (equivalente al «Diseño de impresión» de Word)". La clave del examen marcaba C "Diseño de impresión" (c=2), pero el término correcto en Excel es "Diseño de página" (opción B); c corregido de 2 a 1
ERR       | q_50 (idx 49) | Excel 365 - Atajos de teclado    | Temario Anexo: "CTRL+U | Crear un libro nuevo en blanco". La clave del examen marcaba D "CTRL+N" (c=3), pero CTRL+N es Negrita en Excel español; el atajo correcto es CTRL+U (opción C); c corregido de 3 a 2

## WARN

WARN      | q_07 (idx 6)  | Excel 365 - Guardar              | La clave marca B (CTRL+G) como única opción correcta, pero C (barra de acceso rápido) también contiene Guardar según el temario; D se descarta porque A (barra de estado) es incorrecta
WARN      | q_54 (idx 53) | Excel 365 - Abrir libro          | La clave marca B ("En la pestaña inicio, usar CTRL+A"); CTRL+A es correcto para abrir, pero la pestaña correcta sería Archivo, no Inicio; el atajo funciona desde cualquier pestaña
WARN      | q_137 (idx ~) | Excel 365 - Filtro               | La clave marca C (Inicio) para la ubicación de Filtro; el temario lo sitúa en "Inicio > Buscar y seleccionar" (Ordenar y filtrar) y también en la pestaña Datos; ambas son válidas

## Detalle selectivo (preguntas del test 129, todas nuevas)

OK        | q_169 (test 129 #1) | Excel 365 - Barra de fórmulas | Temario §4.1: "se cancela con ESC o con el botón rojo ✕" — icono X anula datos; c=0 correcto
OK        | q_170 (test 129 #2) | Excel 365 - ESC                | Temario §4.1: "se cancela con ESC" — coincide; c=2 correcto
OK        | q_171 (test 129 #3) | Excel 365 - Barra de estado    | Temario §4.1: "Tras confirmar, el modo vuelve a Listo" — coincide con C; c=2 correcto
OK        | q_172 (test 129 #4) | Excel 365 - Alineación         | Temario §4.2: "Texto: se alinea a la izquierda" — coincide con B; c=1 correcto
OK        | q_173 (test 129 #5) | Excel 365 - Fechas             | Temario §4.2: "se alinean a la derecha y se formatean automáticamente" — coincide con B; c=1 correcto
OK        | q_174 (test 129 #6) | Excel 365 - Negativos          | Temario §4: "(10) se interpreta como –10" — coincide con D; c=3 correcto
OK        | q_175 (test 129 #7) | Excel 365 - Función AHORA      | Temario §5.2: "AHORA(): devuelve la fecha y la hora del sistema" — coincide con C; c=2 correcto
OK        | q_176 (test 129 #8) | Excel 365 - Atajos de teclado  | Temario §4.3: "CTRL+; (en el teclado español, CTRL+,)" para fecha estática — coincide con D; c=3 correcto
OK        | q_177 (test 129 #9) | Excel 365 - CTRL+INTRO         | Temario §4.3: "seleccionar el rango, escribir el dato y confirmar con CTRL+INTRO" — coincide con B; c=1 correcto
OK        | q_178 (test 129 #10)| Excel 365 - ALT+INTRO          | Temario §4.3: "salto de línea dentro de la celda: ALT+INTRO" y §9.1: "Ajustar texto: muestra el contenido en varias líneas" — D (B y C correctas) coincide; c=3 correcto

## Resumen

| Veredicto | Cant. | Notas |
|-----------|-------|-------|
| OK        | 173   | Verificadas contra el temario |
| ERR       | 2     | Corregidas (Diseño de impresión→página; CTRL+N→CTRL+U) |
| WARN      | 3     | Guardar con barra acceso rápido; CTRL+A en pestaña inicio; Filtro en Inicio vs Datos |
| REVIEW    | 0     | — |

El JSON es válido y mantiene las 178 preguntas con los mismos campos. Se corrigieron 2 preguntas con certeza total respaldada por citas del temario.
