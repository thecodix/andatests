# Validación Tema 13 — Información general UHU (estructura, centros, departamentos, catálogo de titulaciones)

Fuentes: `.cache/tema13_temario_...txt` (temario oficial, sintetizado) + dos claves oficiales de examen (`.cache/tema13_preguntas_test_121...txt` y `..._test_122...txt`).
Resultado global: los 76 índices `c` del banco coinciden con las claves oficiales de examen. Sin correcciones (0 ERR). No se ha modificado el JSON.

```
OK      | q_01 | Catálogo titulaciones | Temario: "GRADO EN FÍSICA" (F. Ciencias Experimentales); Antropología/Química ambiental no figuran — c=2 (clave 121.1=C)
OK      | q_02 | Catálogo titulaciones | Temario: "GRADO PSICOLOGÍA"; "Ciencias del deporte" real es CAFD, "Geología y medio natural" no existe — c=2 (121.2=C)
OK      | q_03 | Catálogo titulaciones | Temario: doble grado Ing. Eléctrica e Ing. Energías Renovables y Tecnologías Hidrógeno (NUEVO) — c=0 (121.3=A)
OK      | q_04 | Catálogo titulaciones | El triple "ADE, Finanzas y Derecho" no existe en el catálogo — c=1 (121.4=B)
OK      | q_05 | Catálogo/Humanidades  | Temario Humanidades: "Doble Grado en Filología Hispánica y Estudios Ingleses"; "Geografía e Historia" no existe (es Historia) — c=2 (121.5=C)
OK      | q_06 | Catálogo/CC.SS.JJ     | Temario CSJ: "Grado en Educación Primaria"; "Ciencias Jurídicas"/"Contabilidad"/"Educación Especial" no existen — c=1 (121.6=B)
OK      | q_07 | Catálogo titulaciones | Temario: "Doble Grado Ciencias Ambientales e Ingeniería Forestal y del Medio Natural" — c=3 (121.7=D)
WARN    | q_08 | Catálogo/Ingenierías  | Temario cataloga la rama como "Ingenierías", no "Ingeniería y Arquitectura"; opción c=2 es la mejor y la clave (121.8=C)
OK      | q_09 | Catálogo/CC.SS.JJ     | Temario CSJ: "Doble Grado en ADE y Derecho"; los otros dobles no existen — c=0 (121.9=A)
OK      | q_10 | Catálogo titulaciones | "Enfermería y Medicina" no es doble grado; ADE+Turismo, EEII+Fil.Hispánica y Geología+CC.Amb. sí existen — c=2 (121.10=C)
OK      | q_11 | Catálogo/ramas        | Trabajo Social está en "Ciencias Sociales y Jurídicas"; Farmacia no se oferta — c=3 (121.11=D)
OK      | q_12 | Catálogo/Ciencias     | Temario Ciencias y Salud: "Grado en Ciencias Ambientales"; Botánica/Biología no existen — c=0 (121.12=A)
OK      | q_13 | Catálogo titulaciones | Temario: "GRADO EN MEDICINA" (F. Enfermería); Arquitectura/Bellas Artes no — c=2 (121.13=C)
OK      | q_14 | Catálogo/ramas        | Temario: Psicología en "Ciencias y Ciencias de la Salud" — c=0 (121.14=A)
OK      | q_15 | Catálogo/CC.SS.JJ     | Temario: RR.LL. y RR.HH. en rama CSJ (presencial y virtual) — c=1 (121.15=B)
OK      | q_16 | Catálogo/Humanidades  | Temario: "Grado Estudios Ingleses" y doble grado EEII+Fil.Hispánica en Humanidades; Gestión Cultural virtual sí existe — c=2 (121.16=C)
OK      | q_17 | Catálogo/CC.SS.JJ     | Temario: Educación Primaria en "Ciencias Sociales y Jurídicas" — c=1 (121.17=B)
OK      | q_18 | Catálogo titulaciones | Temario Ingenierías: "Doble Grado Ing. Electrónica Industrial e Ing. Mecánica" — c=1 (121.18=B)
OK      | q_19 | Catálogo titulaciones | Temario oferta "GRADO EN GEOLOGÍA"; C.Políticas/C.Comunicación no — c=2 (121.19=C); matiz "(Dual)" no explícito en temario
OK      | q_20 | Catálogo/CC.SS.JJ     | Temario CSJ: "Grado en Derecho"; Económicas/Sociología no existen como tales — c=0 (121.20=A)
OK      | q_21 | Catálogo titulaciones | Criminología no figura en el catálogo UHU → "nada de lo anterior" — c=3 (121.21=D)
OK      | q_22 | Catálogo/Ingenierías  | Temario: "GRADO EN INGENIERÍA FORESTAL Y DEL MEDIO NATURAL" (ETSI); Ing. Agraria/Arq. técnica no — c=2 (121.22=C)
REVIEW  | q_23 | Servicios UHU         | Temario no describe "Formación Permanente"; clave oficial 121.23=A. No localizo el pasaje que lo distinga del SOIPEA; se respeta la clave
OK      | q_24 | Campus UHU            | Temario: campus El Carmen, La Merced, La Rábida, Cantero Cuadrado; el Rectorado es edificio — c=2 (121.23bis=C)
OK      | q_25 | Servicios UHU         | Temario: Lenguas Modernas en "Edificio Juan Agustín de Mora", Campus El Carmen — c=0 (121.24=A)
WARN    | q_26 | Servicios UHU         | Clave oficial 121.25=B (Lenguas Modernas) para "planes de internacionalización"; poco intuitivo frente a Alianzas Internacionales, se respeta la clave
OK      | q_27 | Servicios UHU         | Temario: "Cooperación Internacional" es servicio del Vic. de Igualdad — c=2 (121.26=C)
WARN    | q_28 | Servicios UHU         | Temario tiene servicio "Títulos de Grado y Máster Oficial" (Vic. Ord. Académica); entre las opciones la clave 121.27=D (Gestión Académica)
REVIEW  | q_29 | Servicios UHU         | Temario lista "Enseñanza Virtual" como servicio pero no menciona videoconferencias; clave 121.28=C. Frente a Aula Virtual se respeta la clave
OK      | q_30 | Servicios UHU         | Temario: la agencia de colocación nº0100000014 es del SOIPEA, no del SACU — c=0 (121.29=A)
OK      | q_31 | Servicios UHU         | SACU gestiona/difunde info a la comunidad universitaria; clave 121.30=B (TUO no aparece literal en temario) — c=1
OK      | q_32 | Servicios UHU         | Temario Defensoría: interviene ante "mal funcionamiento que lesiona sus derechos o intereses legítimos" — c=3 (121.31=D)
OK      | q_33 | Servicios UHU         | Temario: Cultura en "Edif. Zenobia Camprubí... Campus de El Carmen" — c=0 (121.32=A)
OK      | q_34 | Servicios UHU         | Prevención de Riesgos: vigilancia salud + residuos + prevención accidentes; clave 121.33=D — c=3
OK      | q_35 | Servicios UHU         | Temario: "PREVENCIÓN DE RIESGOS LABORALES Ubicación: C/ Doctor Cantero Cuadrado, 6" — c=2 (121.34=C)
OK      | q_36 | Servicios/Edificios   | Servicios de SACU/Igualdad en "Edificio Juan Agustín de Mora"; clave 121.35=C — c=2
OK      | q_37 | Edificios UHU         | "Paseo de las Letras" no es edificio UHU; clave oficial 121.36=C — c=2
OK      | q_38 | Servicios UHU         | Temario: Gerencia tiene "Área de Contratación e Infraestructura"; clave 121.37=B (Cantero Cuadrado) — c=1
OK      | q_39 | Edificios UHU         | Clave oficial 121.38=A (Campus del Carmen); no localizado en temario, confirmado por clave — c=0
OK      | q_40 | Edificios UHU         | Clave oficial 121.39=C (Jacobo del Barco); no localizado en temario, confirmado por clave — c=2
OK      | q_41 | Servicios UHU         | Temario: "Servicio de Informática y Comunicaciones (SIC)" en Edificio Alan Turing — c=1 (121.40=B)
OK      | q_42 | Organización UHU      | Temario: Gerencia servicios vinculados "-Servicio de Recursos Humanos" — c=2 (122.1=C)
OK      | q_43 | Organización UHU      | Temario: el Rector preside Consejo de Gobierno y Claustro; el Consejo Social lo preside la Com. Autónoma — c=2 (122.2=C)
WARN    | q_44 | Organización UHU      | B verbatim: "órganos unipersonales que colaboran con el Rector"; A añade "haya prestado" (temario: "que presten servicios") y C es falsa — c=1 (122.3=B)
OK      | q_45 | Organización UHU      | Temario: "Innovación docente" pende del Vic. de Formación y Desarrollo Prof. (no de Ord. Académica), luego C es falsa; clave 122.4=D — c=3
OK      | q_46 | Organización UHU      | Temario Consejo Social: objetivo "Ser los interlocutores entre la universidad y la sociedad" — c=0 (122.5=A)
OK      | q_47 | Organización UHU      | Temario: los centros son Facultades y la ETSI; "Filosofía y Letras"/"Escuela Politécnica"/La Rábida no lo son — c=3 (122.6=D)
OK      | q_48 | Organización UHU      | Temario: Escuela de Doctorado en "Vic. de Doctorado, Política Lingüística y Biblioteca" — c=1 (122.7=B)
OK      | q_49 | Servicios UHU         | Temario: "Oficina de Transferencia de Conocimiento (OTC)" (Vic. Transferencia) — spin-offs — c=2 (122.8=C)
OK      | q_50 | Organización UHU      | Temario: "Vicerrectorado de Formación y Desarrollo Profesional"; los otros nombres no existen — c=0 (122.9=A)
REVIEW  | q_51 | Edificios UHU         | Clave oficial 122.10=D (ninguno en Campus del Carmen); temario no detalla ubicación de CIQSO/CIDERTA/F.Empresariales
OK      | q_52 | Edificios UHU         | Temario: "Oficina Registro General Auxiliar Edificio Juan Agustín Mora Campus de El Carmen" — c=1 (122.11=B)
OK      | q_53 | Organización UHU      | Temario: Claustro = Rector, Sec.Gral, Gerente y 252 repr.; "sectores de la sociedad" son del Consejo Social — c=2 (122.12=C)
OK      | q_54 | Organización UHU      | Temario: Secretaría General servicios vinculados "-Asesoría Jurídica" — c=3 (122.13=D)
OK      | q_55 | Catálogo titulaciones | Temario: F. Educación, Psicología y CC. Deporte incluye "GRADO EDUCACIÓN SOCIAL" (Pedagogía es depto.) — c=2 (122.14=C)
WARN    | q_56 | Departamentos UHU     | Clave 122.15=B (Derecho Público y del Trabajo), pero temario también lista "Ciencias Integradas" como depto. → dos opciones válidas (A y B)
OK      | q_57 | Servicios UHU         | Temario: Lenguas Modernas en Campus El Carmen — c=2 (122.18=C)
OK      | q_58 | Catálogo titulaciones | Temario: "GRADO EN INGENIERÍA MINERA (NUEVO)"; opción A es nombre de departamento — c=3 (122.20=D)
OK      | q_59 | Catálogo titulaciones | Temario: F. Enfermería imparte "GRADO EN ENFERMERÍA" y "GRADO EN MEDICINA"; Fisioterapia/Farmacia no — c=2 (122.21=C)
OK      | q_60 | Estatutos/Juntas      | Temario: Juntas de Centro "incluidos los natos, no inferior a 20 ni superior a 80" — c=1 (122.22=B)
OK      | q_61 | Estatutos/Claustro    | Temario: "representantes del alumnado... elegidos por un mandato de dos años" — c=0 (122.23=A)
OK      | q_62 | Estatutos/C.Gobierno  | Temario: Consejo de Gobierno "el Rector o Rectora, que lo preside" — c=1 (122.24=B)
OK      | q_63 | Organización UHU      | Temario: Vic. de Investigación y Planificación Estratégica → "Oficina para la gestión y tratamiento de datos" — c=2 (122.25=C)
OK      | q_64 | Departamentos UHU     | Temario: "Ingeniería Electrónica, de Sistemas Informáticos y Automática" — c=1 (122.27=B)
OK      | q_65 | Catálogo titulaciones | Temario: F. Educación no incluye "Psicopedagogía" (sí Ed. Infantil y Psicología) — c=0 (122.28=A)
OK      | q_66 | Servicios UHU         | Colombus = catálogo de la Biblioteca Universitaria; clave oficial 122.30=C — c=2
OK      | q_67 | Organización UHU      | Temario: "Gestión de Personal Docente" en Vic. de Ordenación Académica y Profesorado — c=0 (122.31=A)
OK      | q_68 | Organización UHU      | Temario Vic. Estudiantes lista "Participación y Representación Estudiantil", no "Gobierno y Representación" — c=3 (122.32=D)
OK      | q_69 | Organización UHU      | Temario: Secretaría General servicios "-Órganos Colegiados" — c=2 (122.33=C)
OK      | q_70 | Servicios UHU         | "Mayores de 55" es el ámbito del Aula de la Experiencia, no vía de acceso; clave 122.34=C — c=2
OK      | q_71 | Edificios UHU         | Clave oficial 122.35=D (Vicente Ferrer Moncho); no localizado en temario, confirmado por clave — c=3
REVIEW  | q_72 | Edificios UHU         | Pregunta encadenada al comedor; clave 122.36=D; sin dato en temario para verificar ubicación
OK      | q_73 | Servicios UHU         | Temario ubica OGI/OTC/Editorial en "Edificio Marie Curie"; clave 122.37=D (UCC+i) — c=3
OK      | q_74 | Servicios UHU         | Temario: "Unidad para la Calidad" (Vic. Calidad y Concursos Docentes) — c=0 (122.38=A)
OK      | q_75 | Organización UHU      | Temario: Vic. de Proyección Universitaria → "Dirección del Museo Pedagógico / -Museo Pedagógico" — c=0 (122.39=A)
OK      | q_76 | Organización UHU      | Temario Vic. Igualdad no incluye "Aula de sostenibilidad" (sí Igualdad, Salud, Inclusión, Cooperación) — c=2 (122.40=C)
```

## Resumen
- OK: 67
- ERR (corregidas): 0
- WARN: 5 (q_08 rama "Ingenierías" vs "Ingeniería y Arquitectura"; q_26 internacionalización→Lenguas Modernas contraintuitivo; q_28 opción "Títulos Grado/Máster" ausente; q_44 opción A cuasi-verdadera; q_56 doble opción válida A y B)
- REVIEW: 4 (q_23, q_29, q_51, q_72; datos no localizados en el temario sintetizado, se respeta la clave oficial de examen)

Nota: varios campos `exp` conservan la coletilla "revisar en validación" del generador; todos quedan confirmados por la clave oficial de examen y no se han modificado por no constituir error factual.
