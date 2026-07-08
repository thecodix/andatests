# Validación tema 12 — RD 822/2021

Auditadas 208 preguntas contra `.cache/tema12_temario_tema_12.txt` (RD 822/2021, arts. 1-20).

## Resumen
- OK: 200
- ERR (corregidas): 0 (solo se corrigieron 3 explicaciones engañosas, sin cambiar `c`)
- WARN: 2
- REVIEW: 6

## Preguntas marcadas por el generator (verificadas)

FIX-EXP  | q_62 (TEST 115 Q17) | Art. 5.5 RD 822/2021 | Temario: "un convenio que será incorporado a la memoria"; la opción A dice "que podrá incorporarse" → clave D CORRECTA. Exp actualizada.
REVIEW   | q_40 (TEST 102 Q39) | Art. 17.4 RD 822/2021 | Temario: TFM "un máximo de 30"; opciones 42/"créditos según los casos"/24/6 — ninguna es 30. Clave C (24) es errónea y no hay opción válida (opción B truncada). Requiere reconstrucción manual.
REVIEW   | q_171 (TEST 66 Q35) | Art. 10.5 RD 822/2021 | Temario: "no podrá superar, globalmente, el 15 por ciento"; ninguna opción lo enuncia. Clave A ("podrá superar el 10%") es errónea; sin opción correcta. Requiere reconstrucción manual.
FIX-EXP  | q_177 (TEST 66 Q41) | Art. 11.2 RD 822/2021 | Temario: "pudiéndose concretar en materias... obligatorias u optativas"; opción B dice "deberán", opción C añade "básicas" → clave D CORRECTA. Exp actualizada.
FIX-EXP  | q_198 (TEST 66 Q63) | Art. 14.7 RD 822/2021 | Temario: "tecnologías digitales de la información y la comunicación"; opción B dice "de formación", opción C dice 70% (ley: 80%) → clave D CORRECTA. Exp actualizada.

## Otras incidencias

REVIEW   | q_37  | Art. 16.1 RD 822/2021 | Temario: "temáticamente o multidisciplinar"; la opción B (clave) dice "temáticamente o interdisciplinar". Es la respuesta intencionada (única con "temáticamente"), pero el texto de la opción cambia "multidisciplinar" por "interdisciplinar". No modifico `c`; posible errata de opción.
REVIEW   | q_129 | Ref. dice "Art. 9"    | El contenido (movilidad, reconocimiento y transferencia de créditos) corresponde al Art. 10.1, no al 9. Enunciado y ref citan art. 9; respuesta c=2 correcta. Recomiendo corregir ref/enunciado a Art. 10.
REVIEW   | q_165 | Ref. dice "Art. 8"    | El contenido (créditos formato ECTS) corresponde al Art. 9.1, no al 8. Enunciado y ref citan art. 8; respuesta c=2 (ECTS) correcta. Recomiendo corregir ref/enunciado a Art. 9.
WARN     | q_176 | Art. 11.2 RD 822/2021 | Prácticas externas son "curricular y extracurricular"; ninguna opción lo dice completo. La clave (C, "externas... extracurricular") es la menos incorrecta. Opciones ambiguas.
WARN     | q_138 | Art. 1.2 RD 822/2021  | "Nada de lo anterior" (c=3) por matiz "planes de estudios" vs "oferta académica" en opción C. Correcto pero exige lectura muy fina.

## Notas
- Las 3 correcciones de explicación (q_62, q_177, q_198) confirman que la clave D era correcta: el generator había leído los distractores como si fueran texto literal, pero cada uno altera una palabra clave (será→podrá, deberán→pudiéndose, información→formación).
- Los 2 REVIEW defectuosos (q_40, q_171) tienen clave errónea confirmada pero SIN opción correcta disponible; no se pueden corregir con certeza sin reescribir opciones.
- El resto de preguntas (arts. 1-20) verificadas una a una contra el temario: correctas.
- JSON válido tras la edición: 208 preguntas, campos {q,o,c,ref,exp} intactos.
