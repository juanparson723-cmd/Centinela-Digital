# Centinela Digital

**Construye aplicaciones web · Proyecto laboral · Práctica 4: Prototipos interactivos**

| | |
|---|---|
| **Institución** | CECYTEM (Colegio de Estudios Científicos y Tecnológicos del Estado de México) |
| **Carrera** | Programación |
| **Semestre / Turno** | Quinto / Matutino |
| **Docente** | Zita Concepción Álvarez Cruz |
| **Equipo 3** | Dávila López Fernando Sotero · García Pérez Merari de los Ángeles · Blanca Esther Mendieta Ignacio · Mendoza Garrido Osvaldo Alonso · Ramírez Valverde Karen Itzel · Ávila Martínez Leslie Lucero |

---

## 1. Descripción del proyecto

**Centinela Digital** es una aplicación web pensada para que las personas de nuestra comunidad puedan **realizar denuncias y reportar situaciones de violencia, abuso, delitos** o cualquier problema que afecte su seguridad. Además, ofrece un directorio de instituciones que pueden brindar ayuda.

El objetivo de esta práctica fue documentar el proceso de diseño de la plataforma antes de programarla. Se trabajó en cuatro etapas:

1. Crear la **guía de estilo** del proyecto.
2. Crear los **prototipos de baja fidelidad** en Balsamiq.
3. Crear los **prototipos de alta fidelidad** en Figma.
4. Documentar todo el proceso en este **README**.

---

## 2. Herramientas utilizadas

| Herramienta | Uso en el proyecto |
|---|---|
| **Balsamiq** | Bocetos de baja fidelidad: permiten organizar la estructura de las pantallas, botones, menús, imágenes y formularios sin preocuparse por el diseño final. |
| **Figma** | Prototipos de alta fidelidad: muestran colores, tipografías, imágenes y navegación con una apariencia cercana al producto final. Permite trabajo colaborativo en tiempo real. |
| **Coolors** | Generación de la paleta de colores. |

---

## 3. Etapa 1: Guía de estilo

La guía de estilo define la identidad visual de Centinela Digital. Como el proyecto aún está en planeación y sin desarrollo, esta fase se centró en las bases gráficas.

### 3.1 Logotipo

El nombre "Centinela" representa **guardia y vigilancia**. Esa idea se llevó a un **escudo** como elemento principal (protección y seguridad), que contiene un **teléfono móvil con signo de exclamación**, una **mano interactuando con la pantalla** y la figura de un **oficial**, para representar la parte digital del nombre.

El logotipo se analizó con 12 criterios de diseño:

1. Tipografía secundaria ("Centinela" complementa el diseño principal)
2. Símbolo representativo (guardia y vigilancia)
3. Tipografía principal (la palabra "Digital" usa una tipografía moderna y tecnológica)
4. Jerarquía tipográfica ("Centinela Digital" tiene el mayor tamaño y peso visual)
5. Elemento gráfico (el escudo refuerza protección y seguridad)
6. Simplicidad (pocos elementos y formas limpias)
7. Composición equilibrada (escudo, teléfono y texto distribuidos de forma armoniosa)
8. Paleta de colores (tonos de azul y rojo, coherentes con seguridad y tecnología)
9. Tipografía secundaria ("Digital" con un tono diferente que complementa el nombre)
10. Contraste (colores oscuros sobre fondo claro para facilitar la lectura)
11. Identidad clara (comunica una agencia de seguridad digital moderna)
12. Memorabilidad (la combinación de escudo, policía y teléfono es única y fácil de recordar)

### 3.2 Paleta de colores principal

Se eligió una paleta de cinco colores (obtenida de Coolors) para que el sitio se relacione visualmente con las páginas oficiales de denuncia en México, tenga un aire formal y transmita seriedad.

| Color | Código | Uso |
|---|---|---|
| Vinotinto | `#780000` | Carácter de alerta, énfasis |
| Rojo | `#C1121F` | Botones de acción |
| Beige | `#FDF0D5` | Fondo neutro que equilibra el conjunto |
| Azul marino | `#003049` | Encabezados, formalidad |
| Azul claro | `#669BBC` | Tecnología, apoyo visual |

### 3.3 Colores secundarios

| Color | Código | Uso |
|---|---|---|
| Neutro principal (gris oscuro) | `#2B2D2F` | Texto sobre fondos claros; se eligió en lugar del negro puro para evitar la fatiga visual |
| Estado de seguridad / correcto (verde) | `#0E9B56` | Marcas de verificación, mensajes de confirmación, estados exitosos |
| Estado de alerta / advertencia (amarillo) | `#FFBF00` | Precaución sin alarmar: avisos de riesgo medio, alertas no críticas |
| Acento de fondo / profundidad (azul-negro) | `#010618` | Menús laterales, encabezados de tablas, tarjetas destacadas |

### 3.4 Ejemplos de diseño

Se realizaron dos simulaciones de la ventana de inicio con la misma paleta pero con los colores en distintos lugares, para evaluar con cuál se sentiría más cómodo el usuario. También se mostró un ejemplo de la sección de reportes, que resalta lo más importante: mapa interactivo, formulario de reporte, noticias de impacto de los últimos 30 días y casos resueltos.

### 3.5 Tipografías (todas gratuitas)

| Tipografía | Estilo | Uso | Pesos |
|---|---|---|---|
| **Montserrat** (principal) | Moderna, sólida y profesional | Nombre "Centinela Digital", títulos y encabezados de tarjetas | Bold 700, ExtraBold 800 |
| **Poppins** (secundaria) | Amigable, redondeada y accesible | Botones ("Realizar una denuncia", "Iniciar sesión"), menú y etiquetas | Medium 500, SemiBold 600 |
| **Open Sans** (lectura) | Clara, neutral y fácil de leer | Descripciones, instrucciones, avisos de privacidad, mensajes de confianza | Regular 400 |

### 3.6 Jerarquía tipográfica

| Elemento de la página | Tipografía | Peso |
|---|---|---|
| Centinela Digital | Montserrat | ExtraBold 800 |
| Título principal | Montserrat | Bold 700 |
| Menú de navegación | Poppins | Medium 500 |
| Botones de denuncia | Poppins | SemiBold 600 |
| Títulos de categorías | Montserrat | Bold 700 |
| Descripciones | Open Sans | Regular 400 |
| Avisos de privacidad | Open Sans | Regular 400 |

### 3.7 Colores semánticos

Transmiten un significado de forma intuitiva, sin que el usuario tenga que leer un texto.

| Color | Significado | Aplicación |
|---|---|---|
| **Verde** | Éxito, seguridad, confirmación | Acciones completadas correctamente, estados activos validados |
| **Amarillo / naranja** | Advertencia, precaución | Riesgos medios, notificaciones pendientes, revisiones necesarias |
| **Rojo** | Error, peligro, urgencia | Fallas críticas, campos obligatorios vacíos, acciones destructivas (eliminar, cancelar) |
| **Azul** | Información, guía, neutralidad | Enlaces, elementos interactivos, pestañas activas, instrucciones generales |

### 3.5 Estados de interacción de los botones

Se definieron cuatro estados para los botones (ejemplos: *Crear reporte*, *Iniciar sesión*, *Enviar reporte*):

| Estado | Descripción |
|---|---|
| **Normal (reposo)** | Apariencia inicial; transmite estabilidad y disponibilidad. |
| **Hover (sobreposición)** | Cambio sutil de tono al pasar el cursor; confirma que el elemento es interactivo. |
| **Activo (presionado)** | Cambio inmediato al hacer clic; confirma que la acción fue detectada y evita clics repetidos. |
| **Deshabilitado** | Se ve atenuado cuando la acción no se puede realizar (por ejemplo, faltan datos en el formulario). |

### 3.9 Conclusión de la guía

Se estableció una base sólida de identidad visual: un logotipo memorable, una paleta justificada y funcional, y una distribución tipográfica ordenada que facilitará el trabajo de maquetación cuando el proyecto pase a la fase de desarrollo.

---

## 4. Etapa 2: Prototipos de baja fidelidad (Balsamiq)

Los bocetos en Balsamiq definen la **estructura** de cada pantalla. Cada pantalla se vincula con los requerimientos del proyecto.

> **Acceso al prototipo:** escanea el código QR de Balsamiq.
>
> ![Se encuentra dentro de la carpeta junto con este archivo como qr-balsamiq]

### Dónde se encuentra cada requerimiento (baja fidelidad)

**RF** = requerimiento funcional · **RNF** = requerimiento no funcional

| # | Pantalla | Tipo | Requerimientos | Qué cubren |
|---|---|---|---|---|
| 1 | **Ventana de inicio** | No funcional | RNF-21, RNF-22, RNF-26 | Interfaz clara para crear, consultar o actualizar información; navegación consistente entre funciones; estructura visual consistente entre módulos. |
| 2 | **Novedades de la semana** | Funcional | RF-117 | Generar estadísticas por periodo al seleccionar un intervalo de fechas para consultar información histórica. |
| 3 | **Instituciones visitadas con más frecuencia** | Funcional | RF-41 | Consultar el directorio de instituciones para identificar una instancia de atención para un caso. |
| 4 | **Ventana de casos actuales y novedades** | Funcional | RF-118, RF-19 | Reportes de atención (casos atendidos, canalizados, activos o cerrados) y consulta del estado inicial de un reporte con su identificador. |
| 5 | **Ventana caso específico** (violencia familiar, violencia femenina, abuso infantil, acoso sexual, acoso laboral, acoso escolar) | Funcional | RF-19, RF-64 | Consulta del estado de un reporte y visualización de los datos relevantes del caso al abrir el expediente. Cada tipo de caso tiene su propia pantalla con descripción y botón "Realizar denuncia". |
| 6 | **Formulario de denuncia individual por caso** | Funcional | RF-01, RF-02, RF-03, RF-04, RF-11 | Registrar un nuevo reporte; elegir identificación anónima o identificada; registrar datos personales; capturar la descripción del incidente; validar campos obligatorios. |
| 7 | **Ventana inicio de sesión** | No funcional | RNF-01, RNF-02, RNF-03, RNF-06 | Almacenamiento seguro de contraseñas; autenticación para funciones administrativas; control de acceso basado en roles; expiración e invalidación de sesiones. |
| 8 | **Ventana formulario denuncia** (versión completa) | Funcional y no funcional | RF-01 a RF-12, RNF-23, RNF-30 | Registro del reporte, tipo de identificación, datos personales, descripción, fecha y hora (RF-05), ubicación por geolocalización (RF-06) o manual (RF-07), carga de fotos (RF-08), audios (RF-09) y documentos (RF-10), validación de obligatorios (RF-11) y de formato/tamaño de archivos (RF-12). Etiquetas descriptivas (RNF-23) y corrección de errores antes de confirmar (RNF-30). |
| 9 | **Notificación registro exitoso** | Funcional y no funcional | RF-17, RF-18, RNF-25 | Confirmación de recepción del reporte, identificador de seguimiento y mensaje de confirmación tras una acción importante. |
| 10 | **Ventana instituciones** | Funcional | RF-41, RF-47, RF-48 | Directorio de instituciones, filtro por tipo de servicio y filtro por ubicación. |
| 11 | **Información de la institución** (FGJEM, CEAVEM, DIF, CEPAMyF, CJM, CONAVIM) | Funcional | RF-44, RF-45, RF-46 | Tipos de atención de cada institución, su ubicación y sus medios de contacto (teléfonos, correos, sitios web). |
| 12 | **Historial de denuncias de cada institución** | Funcional | RF-56, RF-58, RF-60 | Historial de canalizaciones de un caso, actualización del estado de una canalización e historial de instituciones involucradas. |

---

## 5. Etapa 3: Prototipos de alta fidelidad (Figma)

Los prototipos de alta fidelidad replican **las mismas pantallas y los mismos requerimientos** de la etapa anterior, pero aplicando la guía de estilo: logotipo con escudo, paleta de colores, tipografías, imágenes reales, tarjetas, botones y navegación.

> **Acceso al prototipo:** escanea el código QR de Figma.
>
> ![Se encuentra dentro de la carpeta junto con este archivo como qr-Figma]

### Dónde se encuentra cada requerimiento (alta fidelidad)

| # | Pantalla | Tipo | Requerimientos |
|---|---|---|---|
| 1 | **Ventana de inicio** (mensaje principal, botón "ingresar como invitado", secciones *vigila / notifica / actúa* y estados de reporte: resuelto, en proceso, urgente) | No funcional | RNF-21, RNF-22, RNF-26 |
| 2 | **Novedades de la semana** | Funcional | RF-117 |
| 3 | **Instituciones visitadas con más frecuencia** | Funcional | RF-41 |
| 4 | **Ventana de casos actuales y novedades** | Funcional | RF-118, RF-19 |
| 5 | **Ventana caso específico** (violencia familiar, violencia femenina, abuso infantil, acoso sexual, acoso laboral, acoso escolar) | Funcional | RF-19, RF-64 |
| 6 | **Formulario de denuncia individual por caso** | Funcional | RF-01, RF-02, RF-03, RF-04, RF-11 |
| 7 | **Ventana inicio de sesión** | No funcional | RNF-01, RNF-02, RNF-03, RNF-06 |
| 8 | **Ventana formulario denuncia** | Funcional y no funcional | RF-01 a RF-12, RNF-23, RNF-30 |
| 9 | **Notificación registro exitoso** | Funcional y no funcional | RF-17, RF-18, RNF-25 |
| 10 | **Ventana instituciones** | Funcional | RF-41, RF-47, RF-48 |
| 11 | **Información de la institución** (FGJEM, CEAVEM, DIF, CEPAMyF, CJM, CONAVIM) | Funcional | RF-44, RF-45, RF-46 |
| 12 | **Historial de denuncias de cada institución** (tabla con tipo de denuncia, estado, evidencias y ubicación) | Funcional | RF-56, RF-58, RF-60 |

---

## 6. Resumen de requerimientos por categoría

### Requerimientos funcionales (RF)

| Grupo | Requerimientos | Pantallas |
|---|---|---|
| Registro de denuncias | RF-01 a RF-12 | Formulario de denuncia (individual y completo) |
| Confirmación y seguimiento | RF-17, RF-18, RF-19 | Notificación de registro exitoso, casos y caso específico |
| Directorio de instituciones | RF-41, RF-44, RF-45, RF-46, RF-47, RF-48 | Instituciones, información de la institución |
| Canalizaciones e historial | RF-56, RF-58, RF-60, RF-64 | Historial de denuncias, caso específico |
| Estadísticas y reportes | RF-117, RF-118 | Novedades de la semana, casos actuales |

### Requerimientos no funcionales (RNF)

| Grupo | Requerimientos | Pantallas |
|---|---|---|
| Seguridad y acceso | RNF-01, RNF-02, RNF-03, RNF-06 | Inicio de sesión |
| Usabilidad y consistencia | RNF-21, RNF-22, RNF-26 | Ventana de inicio |
| Formularios y mensajes | RNF-23, RNF-25, RNF-30 | Formulario de denuncia, notificación de registro exitoso |

---

## 7. Conclusión

Balsamiq y Figma son fundamentales para el desarrollo de Centinela Digital. Los prototipos de **baja fidelidad** permiten representar de forma sencilla la estructura de la plataforma, organizar sus funciones y definir los elementos principales que necesitarán los usuarios. Los prototipos de **alta fidelidad** permiten visualizar con detalle el diseño final: colores, botones, formularios y navegación entre pantallas.

Ambos tipos de prototipos ayudan a identificar errores, realizar mejoras y comprobar que la plataforma sea clara, accesible y fácil de utilizar. Así, Centinela Digital busca ofrecer una propuesta tecnológica que facilite la presentación de denuncias y brinde a los usuarios una experiencia más organizada, segura y confiable.
