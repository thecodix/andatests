# Validación Tema 4 — Recursos administrativos (Ley 39/2015, arts. 121-126)

Fuente de verdad: `.cache/tema4_temario_tema_4.txt` (temario oficial, leído íntegro).
Banco: `banco/tema4.json` (75 preguntas).

Numeración del temario confirmada:
- Art. 121.1 (objeto alzada + Tribunales dependientes); 121.2 (interposición/remisión/informe).
- Art. 124.1 (plazo interposición + "transcurrido, solo contencioso"); 124.2 (plazo resolución 1 mes); 124.3 (no de nuevo).
- Art. 125.1 (causas a-d); 125.2 (plazos: 4 años causa a, 3 meses demás); 125.3 (arts. 106 y 109.2).
- Art. 126.1 (inadmisión motivada sin dictamen); 126.2 (pronunciarse fondo); 126.3 (3 meses desestimado).

## Resumen
- OK: 60
- ERR (corregidas): 13 (todas de referencia legal; ningún índice `c` estaba mal)
- WARN: 2
- REVIEW: 0

## Las 4 preguntas marcadas por el generador — todas con clave D correcta (preguntas trampa)

WARN   | silencio alzada "en todo caso" | Art. 122.2 | Temario: "se podrá entender desestimado el recurso, salvo... artículo 24.1, tercer párrafo" — D correcta: B ("desestimado en todo caso") falla por la excepción; C es defendible pero la clave oficial es D. No modificado.
OK     | prevaricación por "resolución administrativa firme" | Art. 125.2 | Temario art. 125.1.d exige "sentencia judicial firme"; la premisa es falsa → D "nada" correcta. Ref corregida 125.4→125.2.
OK     | inadmisión desestimados "en cuanto a la forma" | Art. 126.1 | Temario: "se hubiesen desestimado en cuanto al fondo" (no forma) → premisa falsa → D correcta. Ref corregida 126.2→126.1.
OK     | inadmisión "sin motivación" | Art. 126.1 | Temario: "podrá acordar motivadamente la inadmisión" → premisa "sin motivación" falsa → D correcta. Ref corregida 126.2→126.1.

## Correcciones de referencia legal (ERR)

ERR    | plazos revisión (x6) | Art. 125.4→125.2 | Temario: los plazos ("cuatro años... En los demás casos... tres meses") están en el apartado 2, no existe 125.4
ERR    | inadmisión motivada (x3) | Art. 126.2→126.1 | Temario apartado 1: "El órgano competente... podrá acordar motivadamente la inadmisión a trámite"
ERR    | pronunciarse sobre el fondo (x1) | Art. 126.3→126.2 | Temario apartado 2: "debe pronunciarse no sólo sobre la procedencia... sino también... sobre el fondo"
ERR    | no interponerse de nuevo reposición (x2) | Art. 124.2→124.3 | Temario apartado 3: "Contra la resolución de un recurso de reposición no podrá interponerse de nuevo dicho recurso"
ERR    | transcurrido plazo, solo contencioso (x1) | Art. 124.3→124.1 | Temario apartado 1: "Transcurrido dicho plazo, únicamente podrá interponerse recurso contencioso-administrativo"
ERR    | Tribunales dependientes (x3) | Art. 121.2→121.1 | Temario apartado 1: "los Tribunales y órganos de selección... se considerarán dependientes del órgano al que estén adscritos"

## Muestra de preguntas OK verificadas

OK     | recurribles en alzada | Art. 121.1 | Temario: "actos... cuando no pongan fin a la vía administrativa, podrán ser recurridos en alzada" — c=2 correcta
OK     | remisión al competente | Art. 121.2 | Temario: "deberá remitirlo al competente en el plazo de diez días, con su informe" — c correcto
OK     | plazo alzada acto expreso | Art. 122.1 | Temario: "será de un mes, si el acto fuera expreso" — c=un mes
OK     | plazo máx. resolución alzada | Art. 122.2 | Temario: "El plazo máximo para dictar y notificar la resolución será de tres meses"
OK     | reposición ante mismo órgano | Art. 123.1 | Temario: "ante el mismo órgano que los hubiera dictado o ser impugnados directamente"
OK     | no contencioso hasta resuelto | Art. 123.2 | Temario: "No se podrá interponer recurso contencioso-administrativo hasta que sea resuelto"
OK     | plazo máx. resolución reposición | Art. 124.2 | Temario: "El plazo máximo para dictar y notificar la resolución del recurso será de un mes"
OK     | revisión contra actos firmes | Art. 125.1 | Temario: "Contra los actos firmes en vía administrativa podrá interponerse el recurso extraordinario de revisión"
OK     | "cualquier resolución judicial firme" es falso | Art. 125.1 | Temario 125.1.d exige "sentencia judicial firme" — c=2 (opción falsa) correcta
OK     | error de hecho, plazo 4 años | Art. 125.2 | Temario: "causa a)... dentro del plazo de cuatro años siguientes a la fecha de la notificación"
OK     | 3 meses desestimado revisión | Art. 126.3 | Temario: "Transcurrido el plazo de tres meses... se entenderá desestimado, quedando expedita la vía... contencioso-administrativa"

WARN   | informe en remisión alzada | Art. 121.2 | Opciones A ("Sí y el expediente") y B ("Sí, del órgano que dictó") ambas defendibles; clave B. No modificado.

Nota: ningún índice de respuesta correcta (`c`) resultó erróneo. Todas las erratas fueron de referencia legal (apartado del artículo), corregidas contra la numeración literal del temario. JSON válido: 75 preguntas, todos los campos presentes. `banco.js` regenerado.
