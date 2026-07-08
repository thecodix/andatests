# Validación tema 16 — Microsoft 365: Word

Temario de referencia: `.cache/tema16_temario_tema16.txt` (redactado por temario-generator, leído íntegro, 10 págs).
Banco: `banco/tema16.json` (196 preguntas). Corregidas: 2 campos `exp` (ninguna clave `c` modificada).

Resumen: 184 OK · 2 ERR (exp corregida) · 2 WARN · 8 REVIEW

```
OK      | q_01 | Esquema numerado      | Temario: "MAYÚS+TABULADOR (sube un nivel)" — coincide con c=2
REVIEW  | q_02 | Lista multinivel      | Depende de imagen no incluida; icono descrito como multinivel, no verificable
OK      | q_03 | Grupo Párrafo         | Temario: viñetas/numeración "en la pestaña Inicio, dentro del grupo Párrafo"
OK      | q_04 | Estilos               | Temario: "el estilo aplicado por defecto es «Normal»"
OK      | q_05 | Estilos               | Temario: "El grupo Estilos se encuentra en la pestaña Inicio"
OK      | q_06 | Estilos               | "Sugerir estilo" no figura; sí Administrar estilos, Mostrar vista previa
OK      | q_07 | Estilo vinculado      | Temario: "combina... un estilo de carácter y un estilo de párrafo"
OK      | q_08 | CTRL+MAYÚS+W          | Temario: "el atajo CTRL+MAYÚS+W, abre el panel... «Aplicar estilos»"
OK      | q_09 | Fuente                | Tipo de letra = fuente
OK      | q_10 | Fuente                | Tachado es efecto de fuente
OK      | q_11 | Grupo Fuente          | Pestaña Inicio
OK      | q_12 | Grupo Fuente          | Formas está en Insertar, no en Fuente
OK      | q_13 | Alineación            | "Superior" no es alineación de párrafo
ERR     | q_14 | CTRL+T                | Temario: "centrada (CTRL+T)" y anexo — c=2 correcto; exp corregida (decía erróneamente "sangría francesa")
OK      | q_15 | Interlineado          | "Doble" es interlineado válido
OK      | q_16 | Tabulaciones          | "Francesa" es sangría, no tabulación
OK      | q_17 | Vistas                | Diseño de impresión se selecciona desde pestaña Vista
OK      | q_18 | Configurar página     | Grupo en pestaña Disposición
WARN    | q_19 | Regla/Sangrías        | Flecha superior = sangría primera línea; coincide con Word pero depende de imagen
OK      | q_20 | Regla/Sangrías        | Temario: regla "muestra los márgenes, las sangrías y las tabulaciones" (no interlineado)
OK      | q_21 | Interfaz de inicio    | "la opción para iniciar un documento nuevo"
OK      | q_22 | Crear documento       | CTRL+N=negrita y "crear"→es Nuevo; ni A ni B crean documento
OK      | q_23 | Crear documento       | Temario: "opción Nuevo"
OK      | q_24 | Plantillas            | Temario: "un buscador de plantillas en línea (a través de Office.com)"
OK      | q_25 | Crear documento       | Temario: nombre por defecto "«Documento1»"
OK      | q_26 | Crear documento       | Opción Nuevo en pestaña Archivo
OK      | q_27 | Crear documento       | Temario: "la pestaña Archivo no debe estar activada"
OK      | q_28 | Barra acceso rápido   | Incluye Guardar
OK      | q_29 | Barra acceso rápido   | Temario: "situada por encima de la cinta de opciones"
REVIEW  | q_30 | Guardar               | Clave dice "Recientes" por defecto; el temario dice "aparece seleccionada la opción Examinar" — contradicción; no modifico (clave de examen consistente, temario autoredactado dudoso)
OK      | q_31 | Guardar               | "Ocultar carpetas" es opción real del cuadro Examinar (no en temario, pero de Windows)
OK      | q_32 | Guardar               | Extensión .docx
OK      | q_33 | Guardar               | Archivo/Guardar como
OK      | q_34 | Autoguardado          | Temario: "se activa automáticamente cuando el documento está almacenado en OneDrive"
OK      | q_35 | Autoguardado          | Temario: "con un simple clic sobre dicho control"
OK      | q_36 | Guardar en la nube    | OneDrive vía Archivo/Guardar como
OK      | q_37 | Portapapeles          | Pincel/brochita = Copiar formato
OK      | q_38 | Portapapeles          | Copiar formato en Inicio
OK      | q_39 | Portapapeles          | Temario: "su atajo... es ALT+CTRL+C"
OK      | q_40 | Portapapeles          | Temario: "almacenar hasta 24 elementos"
OK      | q_41 | Símbolos              | Símbolo en pestaña Insertar
REVIEW  | q_42 | Símbolos              | "25 símbolos predeterminados" no verificable en temario ("un conjunto reducido"); dato de clave
OK      | q_43 | Dictar                | Texto aparece automáticamente al hablar (opción D falsa: Dictar está en Inicio, no Insertar)
OK      | q_44 | Párrafo               | Alineación afecta a párrafos
OK      | q_45 | Párrafo               | Temario: "izquierda (CTRL+Q, valor por defecto)"
OK      | q_46 | Párrafo               | Centrada = igual distancia de ambos márgenes sin alinear
OK      | q_47 | Párrafo               | CTRL+J justifica
OK      | q_48 | Interlineado          | "Exacto" es interlineado válido
OK      | q_49 | Párrafo               | Temario: espaciado = "distancia antes y después de cada párrafo"
OK      | q_50 | Sangrías              | No existe sangría "Central"
OK      | q_51 | Párrafo               | Temario: "Bordes y sombreados... desde el propio grupo Párrafo"
OK      | q_52 | Tabulaciones          | TAB desplaza por las tabulaciones
OK      | q_53 | Buscar                | Temario: "Buscar (atajo CTRL+B)"
OK      | q_54 | Reemplazar            | Temario: "Reemplazar (atajo CTRL+L)"
OK      | q_55 | Buscar                | Temario: "pestaña Inicio, dentro del grupo Edición"
OK      | q_56 | Orientación           | Vertical por defecto
OK      | q_57 | Configurar página     | Pestaña Disposición
OK      | q_58 | Configurar página     | Temario: "una sola sección, la orientación... se aplica a la totalidad"
OK      | q_59 | Configurar página     | Botón Márgenes en Configurar página
OK      | q_60 | Márgenes              | Word permite aplicar la última configuración de márgenes; resto de opciones falsas
OK      | q_61 | Márgenes              | Temario: encuadernación "para documentos que se van a imprimir a doble cara"
OK      | q_62 | Márgenes              | Doble clic en regla vertical abre configurar página; resto falsas
OK      | q_63 | Estilos               | Temario: "conjunto de características de formato"
OK      | q_64 | Estilos               | Grupo Estilos en Inicio
REVIEW  | q_65 | Viñetas               | "símbolos con sangría de primera línea" no confirmado por temario (las viñetas usan sangría francesa/colgante); dato de clave, no modifico
OK      | q_66 | Párrafo               | Numeración en grupo Párrafo
OK      | q_67 | Esquemas              | Temario: "definir un esquema... indicando el estilo de número de cada nivel"
OK      | q_68 | Crear documento       | CTRL+U crea documento (resto de opciones falsas)
OK      | q_69 | Deshacer              | Flecha curva = Deshacer
OK      | q_70 | Deshacer              | Temario: "Deshacer (CTRL+Z)"
OK      | q_71 | Entorno               | Temario: barra de título "muestra el nombre del documento abierto"
OK      | q_72 | Guardar               | Guardar en pestaña Archivo
ERR     | q_73 | Fuentes (tachado)     | Temario: "El tachado dibuja una línea recta a través del texto"; c=0 se mantiene (B='dos líneas'=doble tachado); exp corregida
OK      | q_74 | Fuentes               | Grupo Fuente en Inicio
OK      | q_75 | Fuentes               | Temario: color de fuente "admite... efectos de relleno con degradado"
OK      | q_76 | Fuentes               | Subrayado "solo palabras" no marca espacios
OK      | q_77 | Fuentes               | Temario: "CTRL+S subrayado simple"
OK      | q_78 | Fuentes               | Tachado no es estilo de subrayado
OK      | q_79 | Cinta de opciones     | No existe pestaña "Impresión"
OK      | q_80 | Abrir documento       | Archivo>Abrir, carpeta, documento y clic
OK      | q_81 | Plantillas            | Plantillas sugeridas en Archivo>Nuevo
OK      | q_82 | Plantillas            | Temario: plantillas ".dotx"
OK      | q_83 | Plantillas            | Temario: plantilla personalizada bajo sección "Personal"
OK      | q_84 | Plantillas            | Office.com
OK      | q_85 | Plantillas            | Temario: "hacer clic sobre ella y pulsar el botón Crear"
OK      | q_86 | Párrafo               | Grupo Párrafo en Inicio
OK      | q_87 | Configurar página     | Icono = Orientación (imagen, coherente)
OK      | q_88 | Insertar              | Tabla en pestaña Insertar
OK      | q_89 | Párrafo               | Temario: "centrada (CTRL+T)" — confirma q_14
OK      | q_90 | Estilos               | Grupo Estilos en Inicio
OK      | q_91 | Guardar               | Guardar como permite "Agregar un sitio"
OK      | q_92 | Cerrar documento      | Temario: "no ofrece «Guardar como»"
OK      | q_93 | Diseño                | Marca de agua en pestaña Diseño
OK      | q_94 | Barra de estado       | Temario: barra de estado con "recuento de palabras"
OK      | q_95 | Cerrar documento      | Opción Cerrar en Archivo
OK      | q_96 | Fuentes               | Temario: "CTRL+K cursiva"
OK      | q_97 | Saltos                | Salto de página termina página y pasa a siguiente
OK      | q_98 | Selección             | Temario: "CTRL+E" selecciona todo
OK      | q_99 | Selección             | Temario: puntero a la izquierda + triple clic
WARN    | q_100 | Selección            | c=1 (CTRL) correcto por temario; opciones A y C son idénticas (posible confusión)
OK      | q_101 | Selección            | Clic inicial + MAY + clic final selecciona el rango completo
OK      | q_102 | Exportar             | Temario: "Archivo > Exportar"
OK      | q_103 | Selección            | Temario: párrafo = puntero a izquierda + doble clic
OK      | q_104 | Barra de estado      | Número de página en barra de estado
OK      | q_105 | Tablas               | Grupo Tablas en Insertar
OK      | q_106 | Abrir documento      | Temario: "«Documentos» como acceso directo" en Abrir
REVIEW  | q_107 | Recientes            | "40 documentos" no verificable en temario; dato de clave (Word por defecto 50, configurable)
OK      | q_108 | Saltos               | Icono = Salto de página (imagen, coherente)
OK      | q_109 | Tabla de contenido   | Pestaña Referencias
OK      | q_110 | Buscar               | Temario: "buscar distinguiendo mayúsculas de minúsculas"
OK      | q_111 | Párrafo              | Temario: "derecha (CTRL+D)"
OK      | q_112 | Edición              | Temario: "RETROCESO borra el carácter situado a su izquierda" (la i)
OK      | q_113 | Edición              | Temario: "SUPR borra el carácter situado a la derecha" (la e)
OK      | q_114 | Edición              | Temario: CTRL+RETROCESO borra palabra a la izquierda ("Di")
OK      | q_115 | Edición              | Seleccionar todo en grupo Edición
OK      | q_116 | Vistas               | Temario: "La vista predeterminada... es Diseño de impresión"
OK      | q_117 | Información          | Temario: Archivo>Información con "las propiedades del documento"
OK      | q_118 | Cinta de opciones    | Temario: "mostrar solo pestañas, o pestañas y comandos"
OK      | q_119 | Cinta de opciones    | Temario: "CTRL+F1"
OK      | q_120 | Vistas               | Temario: "Regla... disponible desde la pestaña Vista"
OK      | q_121 | Cinta de opciones    | Se muestra clicando en la parte superior (pestaña)
OK      | q_122 | Cinta de opciones    | Temario: "haciendo doble clic sobre cualquiera de sus pestañas"
OK      | q_123 | Guardar              | Guardar = CTRL+G en Word español
OK      | q_124 | Guardar en la nube   | Archivo/Guardar como/OneDrive
OK      | q_125 | Portapapeles         | Copiar formato en Inicio
OK      | q_126 | Tabla de contenido   | Temario: "identificar y marcar... los títulos principales"
OK      | q_127 | Columnas             | Temario: "pestaña Disposición, dentro del grupo Configurar página"
OK      | q_128 | Imprimir             | CTRL+P
OK      | q_129 | Rehacer              | Temario: "Rehacer (CTRL+Y)"
OK      | q_130 | Vistas               | Cambiar ventana = pasar a otras ventanas abiertas
OK      | q_131 | Número de página     | Temario: "en el mismo grupo que Encabezado y Pie de página" (Insertar)
OK      | q_132 | Guardar              | "Ocultar carpetas" en cuadro Examinar
OK      | q_133 | Párrafo              | "Superior" no es alineación
OK      | q_134 | Entorno              | Fecha/hora no aparece de forma permanente en el entorno
OK      | q_135 | Recientes            | Recientes en panel central al pulsar Archivo
OK      | q_136 | Fuentes              | Temario: "CTRL+N negrita"
OK      | q_137 | Fuentes              | CTRL+S sobre palabra subrayada quita el subrayado
OK      | q_138 | Fuentes              | Doble CTRL+S deja subrayado (imagen; opciones C/D idénticas)
OK      | q_139 | Fuentes              | Temario: "CTRL+MAYÚS+D subrayado doble"
OK      | q_140 | Portapapeles         | Grupo Portapapeles en Inicio
OK      | q_141 | Autoguardado         | Temario: autoguardado en OneDrive/SharePoint
OK      | q_142 | Buscar               | No puede buscar por imágenes (sí saltos, espacios)
OK      | q_143 | Correspondencia      | Sobres en pestaña Correspondencia
REVIEW  | q_144 | Insertar             | Icono depende de imagen no incluida; clave=A (Insertar), no verificable
OK      | q_145 | Revisión             | Revisión al escribir se configura en Archivo>Opciones
OK      | q_146 | Comentarios          | Temario: comentarios "añaden una nota... sobre una parte concreta del texto"
OK      | q_147 | Vistas               | "Diseño ventana" no es una vista
OK      | q_148 | Notas al pie         | Temario: nota al pie "en la parte inferior de la misma página"
OK      | q_149 | Cinta de opciones    | Temario: "no existe una pestaña llamada «Fórmulas», propia de Excel"
OK      | q_150 | Barra de estado      | Temario: modo concentración "se muestra en la barra de estado"
OK      | q_151 | Zoom                 | Zoom acerca/aleja la vista
OK      | q_152 | Ventana              | Icono = Minimizar (imagen, coherente)
OK      | q_153 | Crear documento      | CTRL+U crea documento
OK      | q_154 | Autoguardado         | Botón en barra de acceso rápido
OK      | q_155 | Plantillas           | Archivo>Nuevo para plantillas en línea
OK      | q_156 | Cerrar documento     | Temario: "CTRL+F4 (cierra el documento activo)"
OK      | q_157 | Guardar en la nube   | OneDrive
REVIEW  | q_158 | Fuentes              | Icono depende de imagen; clave=B (nota al pie) pero ref=Fuentes; incoherente sin imagen, no modifico
OK      | q_159 | Temas                | Temario: "un tema es un conjunto único de colores, fuentes y efectos"
OK      | q_160 | Tabla de contenido   | Pestaña Referencias
OK      | q_161 | Pestaña Archivo      | Exportar en Archivo
OK      | q_162 | Deshacer             | Deshacer es CTRL+Z; ninguno de los listados
OK      | q_163 | Guardar              | Examinar muestra ubicaciones para guardar
OK      | q_164 | Reemplazar           | CTRL+L
OK      | q_165 | Administrar documento| Temario: "recuperar documentos que se cerraron sin llegar a guardar"
OK      | q_166 | Selección            | Temario: "Una palabra: doble clic sobre ella"
OK      | q_167 | Selección            | Temario: "Una frase: mantener pulsada CTRL y hacer clic"
OK      | q_168 | Edición              | CTRL+RETROCESO borra palabra a la izquierda del cursor
OK      | q_169 | Cambiar mayúsculas   | Temario: "MAY+F3... alternar entre mayúsculas, minúsculas y tipo oración"
OK      | q_170 | Guardar              | Guardar como en Archivo
OK      | q_171 | Dictar               | Temario contexto: botón Dictar (grupo Voz), pestaña Inicio
OK      | q_172 | Exportar             | Crear PDF/XPS en Archivo>Exportar
REVIEW  | q_173 | Guardar              | Clave: "por defecto... la opción recientes"; temario dice "aparece seleccionada la opción Examinar" — misma contradicción que q_30; no modifico
OK      | q_174 | Historial versiones  | Temario: "Desde Archivo > Información se accede al Historial de versiones"
OK      | q_175 | Historial versiones  | "ver y restaurar versiones anteriores"
OK      | q_176 | Historial versiones  | Temario opciones: Abrir versión, Comparar, Restaurar (no "Revisar")
OK      | q_177 | Historial versiones  | Temario: "Restaurar (convierte la versión anterior... en la versión actual)"
OK      | q_178 | Historial versiones  | Temario: "Comparar (muestra en una misma pantalla las distintas versiones y los cambios)"
OK      | q_179 | Imprimir             | Imprimir en pestaña Archivo
OK      | q_180 | Imprimir             | Atajo es CTRL+P; ninguna de las opciones listadas
OK      | q_181 | Zoom                 | Zoom (Varias páginas) permite ver dos páginas
OK      | q_182 | Imprimir             | Temario: "«4-6» imprime desde la página 4 hasta la 6"
OK      | q_183 | Imprimir             | Temario: desde impresión se accede a márgenes/orientación
OK      | q_184 | Imprimir             | CTRL+P
OK      | q_185 | Tablas               | Temario: tablas "admiten contenido variado (texto, imágenes, gráficos)"
OK      | q_186 | Tablas               | Temario: "Ajuste de texto: Ninguno o Alrededor"
OK      | q_187 | Tablas               | Temario: alineación celda "izquierda, centro, derecha" (no justificar)
OK      | q_188 | Tablas               | Temario: ajuste de texto en "Propiedades de tabla"
OK      | q_189 | Tablas               | Avanzar celda = TAB; ninguna de las opciones dadas
OK      | q_190 | Gráficos             | "Rectángulos" no es tipo de gráfico
OK      | q_191 | Imágenes             | Temario: "pestaña Insertar, grupo Ilustraciones"
OK      | q_192 | Imágenes             | Imágenes no tienen autoformas; resto de opciones falsas
OK      | q_193 | SmartArt             | Temario: "SmartArt: representación gráfica... en forma de organigramas"
OK      | q_194 | Columnas             | Temario: "Columnas se encuentra en la pestaña Disposición"
OK      | q_195 | Columnas             | Temario: "CTRL+MAYÚS+INTRO inserta un salto de columna"
OK      | q_196 | Número de página     | Temario: principio, final, márgenes o posición actual (no "mitad de página")
```

## Notas para revisión posterior

- **q_30 y q_173** (opción por defecto al guardar): las claves de examen coinciden en "Recientes", pero el temario autoredactado afirma que la opción seleccionada por defecto en Guardar como es "Examinar". Como el temario no es oficial y dos preguntas de examen son consistentes, no se han modificado; convendría revisar y, en su caso, corregir el temario (línea "aparece seleccionada la opción Examinar").
- **q_02, q_144, q_158**: dependen de una imagen no incluida en el texto extraído del PDF; no verificables. q_158 además es incoherente (ref "Fuentes" con respuesta "nota al pie").
- **q_42** (25 símbolos) y **q_107** (40 documentos recientes): datos numéricos de la clave no recogidos en el temario.
- **q_65**: la clave marca "viñetas = símbolos con sangría de primera línea"; técnicamente las viñetas usan sangría francesa/colgante. No verificable en el temario; se deja sin tocar.
