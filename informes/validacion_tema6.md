# Validación tema 6 (TREBEP — arts. 1-68)

Fuente de verdad: `.cache/tema6_temario_tema_6.txt` (Tema 6.pdf, 24 págs, leído completo).
Banco: `banco/tema6.json` — 199 preguntas.

Resumen: 6 ERR corregidas, 6 WARN, resto OK. JSON válido (199 preguntas, todos los campos).

## Errores corregidos (ERR)

```
ERR   | q "flexibilización horaria hijos" | Art. 47.2 TREBEP | Temario: "hijos e hijas menores de doce años"; opción B decía "seis años" y ninguna recoge "doce"; c 1 -> 3 (Ninguna)
ERR   | q "traslado al domicilio sin cambio de residencia" | Art. 48.b TREBEP | Temario: "Por traslado de domicilio sin cambio de residencia, un día"; c 3 -> 0 (opción A "Un día")
ERR   | q "permiso en los términos que se determine" | Art. 48.c TREBEP | Temario: funciones sindicales/representación "en los términos que se determine"; c 3 -> 2 (opción C)
ERR   | q "constitución pareja de hecho documento público" | Art. 48.l TREBEP | Temario: "constitución formalizada por documento público de pareja de hecho, quince días"; c 2 -> 0 (opción A "15 días")
ERR   | q "concurrir a pruebas definitivas de aptitud" | Art. 48.d TREBEP | Temario: "durante los días de su celebración"; c 2 -> 0 (opción A)
ERR (exp) | 3 preguntas art. 49 (nacimiento/adopción/progenitor) | Art. 49 a/b/c TREBEP | exp afirmaba falsamente "el art. 49 establece dieciséis semanas"; el temario dice DIECINUEVE; c ya era correcto, exp reescrita
```

Nota: las preguntas de art. 49 sobre "diecinueve semanas" venían marcadas como sospechosas por el generador, pero la clave del examen (diecinueve) es la CORRECTA — el temario art. 49.a/b/c fija diecinueve semanas (32 en monoparentalidad). Solo se corrigió la explicación, no la respuesta.

## Advertencias (WARN) — clave defendible, no se modifica

```
WARN  | q "acatamiento Constitución (art. 62)" | Art. 62.1.c TREBEP | Temario: "Constitución Y, en su caso, del Estatuto"; opción C usa "o" en lugar de "y" -> clave marca D; trampa textual sutil
WARN  | q "tiempo transcurrido sin disfrute permiso nacimiento" | Art. 49 TREBEP | Temario computa servicio efectivo "durante el disfrute"; la pregunta dice "sin disfrute" -> D; negación tramposa
WARN  | q "quién especifica inicio/fin permiso parental" | Art. 49.g TREBEP | Temario: "progenitora, adoptante o acogedora"; opción D "persona acogedora" válida, A "solo progenitor" incorrecta
WARN  | q "faltas parciales violencia de género" | Art. 49.d TREBEP | Temario: totales y parciales justificadas por servicios sociales de atención o de salud; D coherente, opciones muy próximas
WARN  | q "renuncia no aceptada (art. 64)" | Art. 64.2 TREBEP | Temario cita expediente disciplinario/auto de procesamiento/apertura de juicio oral por delito; opciones A-C alteradas -> D
WARN  | q "excepción acceso UE (art. 57)" | Art. 57.1 TREBEP | Temario: "directa o indirectamente... salvaguardia de los intereses"; opciones A-C alteradas -> D
```

## Verificaciones OK destacadas

```
OK    | permiso segundo grado intervención quirúrgica | Art. 48.a | Temario: "segundo grado... cuatro días hábiles" — coincide (c=2)
OK    | permiso parental duración | Art. 49.g | Temario: "no superior a ocho semanas" — coincide
OK    | permiso parental hasta 8 años | Art. 49.g | Temario: "hasta el momento en que el menor cumpla ocho años" — coincide
OK    | cáncer/enfermedad grave hasta 23 años | Art. 49.e | Temario: "hasta que... cumpla los 23 años" — coincide
OK    | discapacidad 65% hasta 26 años | Art. 49.e | Temario: "hasta 26 años si, antes de 23, grado igual o superior al 65%" — coincide
OK    | vacaciones 22 días hábiles; sábados no hábiles | Art. 50 | Temario: "veintidós días hábiles... no se considerarán días hábiles los sábados" — coincide
OK    | cupo discapacidad 7% / 2% intelectual | Art. 59 | Temario: "cupo no inferior al siete por ciento... al menos el dos por ciento... discapacidad intelectual" — coincide
OK    | jubilación forzosa 65 / prolongación 70 | Art. 67.3 | Temario: "sesenta y cinco años... prolongación... hasta setenta años" — coincide
OK    | rehabilitación silencio desestimatorio | Art. 68.2 | Temario: "se entenderá desestimada la solicitud" — coincide
OK    | principios éticos/conducta (arts. 52-54) | Art. 52-54 | Verificados uno a uno contra el listado del temario
```

## Sin localizar con certeza (REVIEW)

```
REVIEW | q "aplicación a personal funcionario de organismos públicos (art. 2)" | Art. 2 TREBEP | La opción marcada "en la misma forma que a los funcionarios de la AGE" no figura literalmente en el temario; el art. 2.1.d) solo lista los organismos públicos como ámbito de aplicación. Clave conservada, sin evidencia para corregir.
```
