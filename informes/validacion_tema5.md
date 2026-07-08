# Validación tema 5 — Ley 40/2015, Régimen Jurídico del Sector Público

Fuente de verdad: `.cache/tema5_temario_tema_5.txt` (temario oficial, arts. 1-53, leído íntegro).
Banco: `banco/tema5.json` (227 preguntas). Numeración de preguntas por orden de aparición (q_01 = primera).

## Correcciones aplicadas (ERR)

Las tres correcciones afectan al campo `exp`: la clave de respuesta (`c`) ya era correcta según el temario, pero la explicación afirmaba un dato legal falso o sembraba una duda infundada.

```
ERR | q_27 | Art. 50.2.b Ley 40/2015 | Temario: "cualquier otro informe preceptivo... plazo máximo de siete días hábiles". exp decía erróneamente "diez días hábiles"; corregido. (La pregunta sigue siendo defectuosa: ninguna opción recoge "máximo de siete días" — la C dice "mínimo".)
ERR | q_81 | Art. 50.2.b Ley 40/2015 | Temario: "plazo máximo de siete días hábiles". c=1 (máximo de siete días) es correcto; exp afirmaba falsamente "art. 50.2.c fija diez días hábiles". Corregido.
ERR | q_147| Art. 9.1 Ley 40/2015     | Temario: "del órgano superior de quien dependa el órgano delegado, si el delegante y el delegado pertenecen a diferentes Ministerios". c=0 (delegado) es correcto; exp dudaba erróneamente hacia "delegante". Corregido.
```

## REVIEW (sospecha, sin certeza para corregir)

```
REVIEW | q_27 | Art. 50.2.b Ley 40/2015 | Pregunta defectuosa: temario "máximo de siete días hábiles"; opción marcada (c=2) dice "mínimo de siete días hábiles". Ningún distractor es exacto. c dejado como en la clave del examen.
REVIEW | q_83 | Art. 1 Ley 40/2015      | Enunciado garbled ("señale la respuesta incorrecta. No es objeto de la ley"): varias opciones "no son objeto". Clave A. No localizo lectura unívoca; no modifico.
REVIEW | q_159| Art. 11.2 Ley 40/2015   | Temario: responsabilidad de dictar actos es "del órgano o Entidad ENCOMENDANTE". Clave marca D ("nada correcto"); la opción A dice "titular encomendante" (dirección correcta pero dice "titular", no "órgano o entidad"). Ambiguo; no modifico.
REVIEW | q_175| Art. 17.2 Ley 40/2015   | Temario exige "la mitad, al menos, de sus miembros". Ninguna opción lo recoge; la marcada (c=2) dice "menos de la mitad". Pregunta sin respuesta correcta; no modifico.
```

## WARN (mejorable, no error factual)

```
WARN | q_49 | Art. 5.1 Ley 40/2015  | Opción correcta (A) añade "y no administrativa", inexacto respecto al temario ("unidades administrativas"); sigue siendo la única con "efectos jurídicos frente a terceros".
WARN | q_64 | Art. 18.2 Ley 40/2015 | Temario: "en la misma reunión o en la inmediata siguiente"; opción A solo cita "inmediata reunión siguiente" (única no falsa).
WARN | q_102| Art. 18.2 Ley 40/2015 | Opción A "En la misma reunión" es cierta pero parcial (temario admite también la inmediata siguiente); única no falsa.
WARN | q_121| Art. 46.3 Ley 40/2015 | Truco de examen: enunciado dice "software" en vez de "documentos"; clave D. El Esquema Nacional de Seguridad sí sería correcto para "documentos" (cf. q_227).
WARN | q_138| Art. 5.2 Ley 40/2015  | Temario: "corresponde a cada Administración Pública"; opción marcada D dice "A la AGE, en su caso". Aproximación imperfecta pero es la intención de la clave.
WARN | q_77 | Art. 32.3 Ley 40/2015 | Enunciado cita "art. 33", pero el contenido y el ref son art. 32.3. Imprecisión del enunciado (procede del examen).
```

## Resto

Las 214 preguntas restantes se verificaron OK contra el texto del temario (arts. 1-53). Muestras de evidencia:

```
OK | q_02 | Art. 47.1 Ley 40/2015 | Temario: "organismos públicos y entidades de derecho público vinculados o dependientes o las Universidades públicas... para un fin común" — coincide (opción con "organismos públicos", no "órganos").
OK | q_03 | Art. 47.2.a Ley 40/2015 | Temario: "Quedan excluidos los convenios interadministrativos suscritos entre dos o más Comunidades Autónomas para la gestión y prestación de servicios propios" — coincide.
OK | q_15 | Art. 48.8 Ley 40/2015 | Temario: "resultarán eficaces una vez inscritos, en el plazo de 5 días hábiles" — coincide.
OK | q_19 | Art. 49.h Ley 40/2015 | Temario: "duración... no podrá ser superior a cuatro años" — coincide.
OK | q_31 | Art. 50.2.e Ley 40/2015 | Temario: "convenios interadministrativos suscritos con las Comunidades Autónomas serán remitidos al Senado" — coincide.
OK | q_66 | Art. 23.2.c Ley 40/2015 | Temario: "amistad íntima o enemistad manifiesta con... representantes legales... que intervengan en el procedimiento" — coincide.
OK | q_72 | Art. 27.4 Ley 40/2015 | Temario: "no serán susceptibles de aplicación analógica" — la afirmación contraria es la incorrecta (c=0).
OK | q_117| Art. 32.8 Ley 40/2015 | Temario: "El Consejo de Ministros fijará el importe de las indemnizaciones" — coincide.
OK | q_227| Art. 46.3 Ley 40/2015 | Temario: soportes con "documentos" cuentan con medidas "de acuerdo con lo previsto en el Esquema Nacional de Seguridad" — coincide.
```

## Resumen

- OK: 214
- ERR (corregidas): 3 (q_27, q_81, q_147 — todas en campo `exp`; las claves `c` ya eran correctas)
- WARN: 6 (q_49, q_64, q_77, q_102, q_121, q_138)
- REVIEW: 4 (q_27, q_83, q_159, q_175) — q_27 aparece también en ERR por el arreglo de exp
- JSON válido: sí (227 preguntas, mismos campos `{q, o, c, ref, exp}`, 4 opciones cada una).
