# Validación Tema 3 — Ley 39/2015 (arts. 54-95)

Fuente de verdad: `.cache/tema3_temario_tema_3_finiki.txt` (temario oficial completo, arts. 54 a 95).
Banco: `banco/tema3.json` — 188 preguntas. Revisadas todas contra el temario.

## Errores corregidos (ERR)

```
ERR  | q_08 (art. 60.2) | c 3->2 | Temario: "así como el lugar, la fecha, fechas o período de tiempo continuado en que los hechos se produjeron" — la orden SÍ expresa el periodo de tiempo (opción C); D era falsa
ERR  | q_44 (art. 82.2) | c 3->0 | Temario: "en un plazo no inferior a diez días ni superior a quince, podrán alegar" — coincide literalmente con la opción A; D era falsa
ERR  | q_89 (art. 66.4) | c 0->1, ref 66.6->66.4 | Temario: "modelos y sistemas de presentación masiva... Estos modelos, de uso voluntario" — son VOLUNTARIOS, no obligatorios; el art. 66.6 (obligatorio) se refiere a modelos específicos de un procedimiento concreto, no a la presentación masiva
```

## Sospechosas del generador que resultan CORRECTAS (clave D válida) — exp depurada

```
WARN | q_29 (art. 71.3) | c=3 OK | Trampa de enunciado: el temario atribuye la responsabilidad a los titulares con función de INSTRUIR ("los titulares... que tengan atribuida tal función [órgano instructor]... responsables directos de la tramitación... y del cumplimiento de los plazos"), pero el enunciado dice "función de RESOLVER"; por eso ninguna opción encaja -> D correcta. Nota "revisar en validación" eliminada del exp
WARN | q_126 (art. 78.2) | c=3 OK | Temario: "con la advertencia... de que el interesado puede nombrar técnicos para que le asistan"; la opción B dice "NO podrá nombrar técnicos" (opuesto), A/C no recogen la advertencia real -> D correcta. Nota "revisar en validación" eliminada del exp
```

## WARN (opciones ambiguas o muy próximas, sin error factual — no modificado)

```
WARN | q_62 (art. 56.3) | Opciones B (depósito de cantidades) y C (retención de ingresos) también aparecen en la lista del art. 56.3; solo D ("embargo preventivo de bienes") es literal. Redacción algo confusa
WARN | q_93 (art. 67.1) | c=3 (D "ninguna"). La opción C "al año de su efecto lesivo" roza lo correcto ("o se manifieste su efecto lesivo"), pero la regla base es "al año de producido el hecho"; D defendible
WARN | q_130 (art. 80.4) | Enunciado invierte la ley ("podrá ser tenido en cuenta" vs "podrá NO ser tenido en cuenta"); la referencia temporal (D "al adoptar la resolución") es la buscada
WARN | q_144 (art. 87) | Opciones A y C son idénticas ("A quince días"); ambas correctas, no confunde el resultado
WARN | q_154 (art. 89.3) | A y B individualmente ciertas; B usa "presuntamente responsable" (en propuesta de resolución es "responsables"), lo que la descarta -> A. Sin "A y B"
WARN | q_161 (art. 90.3) | c=3 (D). La opción A dice "interpone recurso" en vez de "manifiesta su intención de interponer"; matiz que la invalida
WARN | q_167 (art. 91.3) | c=1 (B). B omite "desde que se inició el procedimiento" pero recoge lo del acuerdo; A es falsa ("desde la finalización")
WARN | q_181 (art. 94.5) | c=3 (D). La opción B es casi literal salvo "podrá seguir" frente al "seguirá el procedimiento" de la ley
```

## Observaciones menores (no afectan a la respuesta)

- Varios enunciados citan un artículo en el texto de `q` distinto del real, pero el campo `ref` es correcto y la respuesta no se ve afectada. Ej.: q_06 dice "art. 57" (contenido art. 58, ref correcta), q_12 "art. 63" (art. 64), q_32 "art. 73" (art. 74). No se modifican por ser texto original del examen y no alterar la clave.
- Referencias de subapartado imprecisas pero de artículo correcto (ej. q_09 ref 61.2 siendo 61.4, q_17 ref 66.3 siendo 66.1.b, q_52 ref 88.2 siendo 88.1). No se corrigen al no afectar a la validez de la respuesta.

## Resumen

- Total preguntas: 188 (sin cambio de número).
- OK: 175
- ERR corregidas: 3 (q_08, q_44, q_89)
- WARN: 10 (incluye q_29 y q_126, cuyas claves D se confirman correctas y cuyo `exp` se depuró)
- REVIEW: 0
- JSON válido: sí (188 preguntas, todos los campos {q,o,c,ref,exp} presentes, c en rango 0-3).
- `banco.js` regenerado.
