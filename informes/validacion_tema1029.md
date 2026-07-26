# Validación tema1029 (Oposición 2 — Infancia y Adolescencia II, tema oficial 29)

Fecha: 2026-07-27
Banco: `banco/tema1029.json` (47 preguntas)
Temario: `pdfs/tema1029/temario/*.pdf` (51 páginas, leído completo vía `.cache/tema1029_temario_tema_29_infancia_y_adolescencia_2025.txt`, 2194 líneas)

## Resumen

- **OK** (verificadas con cita literal del temario o conocimiento jurídico consolidado): 42 preguntas
- **WARN** (respuesta plausible pero sin cita literal disponible en el temario proporcionado): 1 pregunta
- **ERR corregidos**: 4 preguntas — se ha corregido el `exp` (y en un caso el propio enunciado) para que sea fiel al texto real del temario. La opción marcada como correcta no ha cambiado en ninguna de ellas.

## Correcciones aplicadas a `banco/tema1029.json`

### 1. Art. 172 CC — cese de la tutela por abandono voluntario (ERR real)

La explicación decía que el cese de la tutela por abandono voluntario en paradero desconocido opera transcurridos **"dos años"**. El temario dice literalmente:

> "que hayan transcurrido **doce meses** desde que el menor abandonó voluntariamente el centro de protección, encontrándose en paradero desconocido."

Los dos años son en realidad el plazo, distinto, para que los progenitores soliciten el cese de la suspensión de la patria potestad (opción D de la misma pregunta). Se ha corregido el `exp` para reflejar el plazo real (doce meses) y aclarar la diferencia con el plazo de dos años de la opción D. La respuesta marcada (opción C, "seis meses", como la afirmación incorrecta) sigue siendo válida, ya que seis meses tampoco coincide con los doce meses reales.

### 2. Art. 14 bis LOPJM — atención en situaciones de urgencia (pendiente de confirmar → resuelto)

El `exp` original decía "pendiente de confirmar contra el temario". Se confirma que el art. 14 bis LOPJM (introducido por la LO 8/2021) establece que la atención en las situaciones de urgencia no está sujeta a requisitos procedimentales ni de forma alguno, coincidiendo con la respuesta ya marcada. Se ha reescrito el `exp` sin la coletilla de pendiente.

### 3. Obligaciones básicas de los centros de acogimiento residencial (pendiente de confirmar → resuelto)

Se ha leído el listado completo de obligaciones básicas del art. 21 LOPJM (proyecto socioeducativo individual, convivencia entre hermanos, acogimiento en la provincia de origen, coordinación con servicios sociales, preparación para la vida independiente, etc.) y **no** incluye "ser parte en los procesos de oposición a las medidas de protección y desamparo" — eso corresponde al Ministerio Fiscal y a la Entidad Pública. Confirma la respuesta ya marcada; se ha reescrito el `exp` sin la coletilla de pendiente.

### 4. Menores internadas con hijos — error factual en el enunciado (seis años → tres años)

El enunciado afirmaba que las menores internadas podrán tener en su compañía a sus hijos **menores de seis años**. El texto real (LORPM/RD 1774/2004) dice:

> "Las menores internadas podrán tener en su compañía, dentro del centro, a sus hijos **menores de tres años**, siempre y cuando: a)... b)... c)... d)..."

Se ha corregido el enunciado ("seis años" → "tres años"). La respuesta marcada (d, "todas son incorrectas") se mantiene, ya que la lógica de la pregunta es correcta: las cuatro condiciones del reglamento (solicitud de la madre, acreditación de filiación, ausencia de riesgo, autorización judicial) se exigen **conjuntamente**, no de forma alternativa, por lo que ninguna de las opciones, tomada aisladamente, constituye por sí sola la condición completa. Se ha reescrito el `exp` para explicar esto sin apelar a "la clave del examen".

## WARN — no verificable con el temario proporcionado

- **Art. 97 Ley 4/2021 — plazo mínimo de seguimiento tras reintegración familiar ("un año")**: el temario desarrolla el plan individualizado de protección (máximo un año) pero no especifica una duración concreta para el seguimiento posterior a la reintegración familiar. La respuesta del banco (marcada como estimación, "un año") no se ha podido confirmar ni refutar con una cita textual de este temario. Se mantiene sin cambios porque coincide con la duración de la figura análoga (el propio plan individualizado) y no hay indicio de que sea incorrecta, pero queda como punto de posible revisión si aparece un temario más detallado.

## Hallazgos confirmados como correctos (muestra representativa, con cita)

| Tema | Cita del temario |
|------|-------------------|
| Art. 18 LOPJM desamparo | la pobreza, por sí sola, no es motivo suficiente para la separación del menor de su familia |
| Art. 19 bis LOPJM retorno | los cuatro requisitos listados no incluyen la exigencia de "dos años de vínculo" |
| Art. 20 bis LOPJM | cooperar con el plan individual es un derecho de los acogedores, no un deber |
| Art. 21 ter LOPJM | medidas de contención no aplicables a menores de catorce años |
| Art. 29 LOPJM | aislamiento provisional, máximo tres horas consecutivas |
| Art. 172 CC | notificación en 48 horas; asunción de tutela suspende la patria potestad; dos años para solicitar cese de la suspensión |
| Art. 172 bis CC | guarda voluntaria, máximo dos años |
| Art. 174 CC | control semestral del Ministerio Fiscal |
| Ley 4/2021 art. 92 | atención inmediata, plazo de tres meses |
| Ley 4/2021 art. 93 | guarda provisional, siete días naturales |
| Ley 4/2021 art. 95 | resolución de desamparo por órgano colegiado (no por la persona titular de la Delegación Territorial); plazo de tres meses |
| Ley 4/2021 art. 97 | plan individualizado de protección, máximo un año |
| Decreto 42/2002 art. 24 | quince días hábiles para alegaciones |
| Decreto 42/2002 art. 26 | diez días hábiles para el trámite de audiencia |
| Ley 4/2021 art. 108 | acogimiento residencial no procede para menores de trece años |
| Decreto 355/2003 art. 31 | veinticuatro horas para comunicar la ausencia a las FCSE |
| Ley 4/2021 art. 132 | programas de vida independiente hasta los veinticinco años |
| Art. 182 CC | conservación de información sobre orígenes durante cincuenta años |
| Art. 7 LORPM | listado completo de medidas (a-ñ), incluida la inhabilitación absoluta, confirmado íntegro |
| Art. 45 LO 5/2000 | competencia de ejecución: Comunidades Autónomas y Ciudades de Ceuta y Melilla |
| RD 1774/2004 art. 10 | programa individualizado, veinte días |
| Art. 56 LORPM | participar en actividades formativas es un deber de los internados, no un derecho |
| Menores internadas con hijos | condiciones a-d del reglamento (ver corrección nº 4 arriba) |

## Conclusión

`banco/tema1029.json` estaba en buen estado general. Se han corregido 4 explicaciones (una de ellas con un error factual real — "dos años" en vez de "doce meses" — y otra con un error en el propio enunciado — "seis años" en vez de "tres años"), y se ha resuelto la incertidumbre de dos ítems previamente marcados como "pendiente de confirmar". Queda una única cuestión (el plazo de seguimiento tras reintegración familiar) sin poder verificarse con el temario disponible, documentada como WARN.
