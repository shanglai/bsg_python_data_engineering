# PROMPT 3 — Generación de slides Marpit por capítulo
# Ejecutar después del Prompt 2
# Ejecutar una vez por capítulo: reemplaza [N] por 1, 2, 3, 4, 5 o 6

## CONTEXTO

Curso "Python para Ingeniería de Datos" de BSG Institute.
Alumnos sin experiencia técnica previa. España latinoamericano (México).
Los Prompts 1 y 2 ya crearon estructura y scripts/notebooks.

Ahora debes generar el archivo de slides Marpit unificado para el capítulo [N].

---

## VARIABLES — ajusta antes de ejecutar

```
CAPITULO = 1          # número del capítulo a procesar (1-6)
```

---

## PASO 1 — Leer archivos fuente

Lee en este orden:

1. **Slides originales** de `bsgfiles/[N]_*_Slides.md` → encoding `latin-1`
2. **Scripts generados** de `scripts/cap[N]/[N]_*_Script.py` → encoding `utf-8`
3. **Sílabo de referencia** → incluido al final de este prompt

Ordena todos los archivos por nombre: sección primero, luego bloque.
Imprime el inventario antes de continuar.

---

## PASO 2 — Estructura del archivo de salida

El archivo final es `slides/cap[N]_completo.md`.

### Frontmatter obligatorio (primera línea del archivo):
```yaml
---
marp: true
theme: bsg
size: 16:9
paginate: true
footer: 'Python para Ingeniería de Datos · Capítulo [N]: [Nombre] · BSG Institute'
---
```

### Orden de contenido:
```
[Frontmatter]
[Slide portada del capítulo]
[Portada sección 1]
  [Bloque 1 completo]
  [Bloque 2 completo]
  ...
[Portada sección 2]
  [Bloque 5 completo]
  ...
```

---

## PASO 3 — Slide de portada del capítulo

```markdown
<!-- _class: title -->
# Capítulo [N]: [Nombre completo]
## [Nombre de la primera sección]

---
```

---

## PASO 4 — Slide de portada de sección

Inserta una antes del primer bloque de cada sección nueva:

```markdown
<!-- _class: section -->
# Sección [S]: [Nombre de la sección]
## [Una oración que describe qué construiremos en esta sección]

**En esta sección aprenderás a:**
- [objetivo 1 en lenguaje simple]
- [objetivo 2 en lenguaje simple]
- [objetivo 3 en lenguaje simple]

**Bloques:**
- Bloque [S.1]: [nombre]
- Bloque [S.2]: [nombre]
- Bloque [S.3]: [nombre]
- Bloque [S.4]: [nombre]

---
```

---

## PASO 5 — Estructura de cada bloque

Para cada bloque, construye las slides en este orden exacto:

### 5.1 — Comentario de navegación (no es slide)
```markdown
<!-- ============================================================ -->
<!-- BLOQUE [N].[S].[B] — [Nombre del bloque]                    -->
<!-- Scripts: scripts/cap[N]/[N]_[S]_[B]_Script.py               -->
<!-- Notebook: notebooks/cap[N]/[N]_[S]_[B]_Script.ipynb         -->
<!-- ============================================================ -->
```

### 5.2 — Slide de apertura del bloque
```markdown
<!-- _class: section -->
# Bloque [N].[S].[B]
## [Nombre del bloque]

> [Una oración que conecta este bloque con el anterior
>  y con el hilo del caso práctico — dataset de transacciones]

**Al terminar este bloque podrás:**
- [objetivo 1 — verbo de acción + resultado concreto]
- [objetivo 2]
- [objetivo 3]

---
```

### 5.3 — Slides de contenido (del archivo original)
Integra las slides del archivo `bsgfiles/[N]_[S]_[B]_Slides.md` original,
respetando el contenido pero aplicando estas mejoras:

**Mejoras obligatorias en cada slide de contenido:**

a) Si la slide tiene un término técnico sin explicar en lenguaje simple,
   añade en itálica justo después de la primera mención:
   *"En palabras simples: [analogía cotidiana en 1 oración]"*
   No repitas la analogía si ya apareció en una slide anterior del mismo bloque.

b) Si la slide tiene bullets sin contexto del caso práctico,
   añade al final un pequeño ejemplo con los campos del dataset
   (`id_transaccion`, `fecha`, `customer_id`, `amount`, `status`, `store`).

c) Mantén todos los bloques de código originales.
   Si el código no tiene comentarios en español, añádelos.
   Máximo 20 líneas de código por slide; si hay más, parte en dos slides.

### 5.4 — Slide de ejemplo del script (si el bloque tiene script)

```markdown
<!-- _class: code -->
## 🧪 Práctica: [Nombre corto de la actividad]

**¿Qué vas a hacer?**
[2-3 líneas explicando la actividad en lenguaje simple]

```python
# [Fragmento más representativo del script — máximo 18 líneas]
# Extraído de: scripts/cap[N]/[N]_[S]_[B]_Script.py
```

**Para ejecutarlo:**
[Badge del entorno correcto — ver Paso 6]

---
```

### 5.5 — Slide de errores comunes
```markdown
## ⚠️ Errores comunes en este bloque

- ❌ **[Error típico de principiante]**
  → [consecuencia en el pipeline]
  → ✅ [cómo evitarlo en 1 línea]

- ❌ **[Segundo error común]**
  → [consecuencia]
  → ✅ [solución]

- ❌ **[Tercer error común]**
  → [consecuencia]
  → ✅ [solución]

---
```

### 5.6 — Slide de cierre del bloque
```markdown
## ✅ Resumen: Bloque [N].[S].[B]

**Lo que aprendiste:**
- [concepto 1 en lenguaje simple]
- [concepto 2]
- [concepto 3]

**Lo que construiste:**
[1 oración describiendo el entregable concreto del script]

**Siguiente paso →** Bloque [N].[S].[B+1]: [Nombre del siguiente bloque]

---
```

---

## PASO 6 — Badges de entorno

Usa el badge correcto en la slide de práctica según el capítulo y bloque:

### Colab (Cap 1, 2, 3 y bloques 4.7.x):
```markdown
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shanglai/bsg_python_data_engineering/blob/main/notebooks/cap[N]/[N]_[S]_[B]_Script.ipynb)
```

### Codespaces (Cap 5, 6 y bloques 4.8.x):
```markdown
[![Abrir en Codespaces](https://img.shields.io/badge/Abrir%20en-Codespaces-blue?logo=github)](https://codespaces.new/shanglai/bsg_python_data_engineering)

*En la terminal del Codespace ejecuta:*
`python scripts/cap[N]/[N]_[S]_[B]_Script.py`
```

### Play with Docker (bloques 4.8.x como alternativa):
```markdown
[▶ Play with Docker](https://labs.play-with-docker.com/) — alternativa sin instalación
```

### Demo sin script (4.7.3, 5.10.3):
```markdown
> 👁️ **Bloque de demostración** — el instructor ejecuta en vivo.
> No hay script para correr en este bloque.
```

---

## PASO 7 — Reglas de calidad del Markdown

Antes de escribir el archivo, verifica cada slide:

1. ✅ Exactamente un H2 (`##`) como primer encabezado de cada slide
2. ✅ No hay slides vacías (solo `---` sin contenido)
3. ✅ Bloques de código con fence correcto (` ```python ` o ` ```bash ` o ` ```sql `)
4. ✅ Máximo 20 líneas de código por slide
5. ✅ Las clases de layout usan solo: `title`, `section`, `code`, `invert`
6. ✅ Ninguna slide tiene más de ~10 bullets (si hay más, parte en dos slides)
7. ✅ Todos los bloques del capítulo están presentes
8. ✅ El orden de secciones y bloques es correcto

Si alguna validación falla: corrígela, reporta qué se corrigió, continúa.

---

## PASO 8 — Guardar y reportar

Guarda el archivo en:
```
slides/cap[N]_completo.md
```
Encoding: `utf-8`

Al finalizar imprime:
```
✅ Archivo generado: slides/cap[N]_completo.md
📊 Total de slides: [N]
📦 Bloques procesados: [lista con nombre de cada bloque]
🆕 Slides añadidas (no estaban en el original):
   - Portadas de sección: [N]
   - Aperturas de bloque: [N]
   - Ejemplos de script:  [N]
   - Errores comunes:     [N]
   - Cierres de bloque:   [N]
⚠️  Advertencias: [lista o "Ninguna"]
```

---

## REFERENCIA — Dataset estándar del caso práctico

```python
# Campos del dataset de transacciones — usar en TODOS los ejemplos
transaccion = {
    "id_transaccion": "TXN-00001",   # str  — identificador único
    "fecha": "2024-01-15",            # str  — ISO YYYY-MM-DD (puede venir sucio)
    "customer_id": 1001,              # int  — ID del cliente (puede ser None)
    "amount": 250.50,                 # float — valor de la venta (puede venir como str)
    "status": "COMPLETADA",           # str  — COMPLETADA|PENDIENTE|FALLIDA|CANCELADA
    "store": "CDMX-Norte"             # str  — sucursal (puede ser None)
}
```

---

## REFERENCIA — Sílabo completo

### Capítulo 1 — Fundamentos de Python aplicado a datos
**Sección 1:** Python para procesamiento de datos
- 1.1.1: Introducción al curso y caso del pipeline
- 1.1.2: Variables, tipos y estructuras básicas
- 1.1.3: Lectura de archivos CSV y primeros scripts
- 1.1.4: Funciones aplicadas a limpieza de datos

**Sección 2:** Pandas y mini ETL
- 1.2.1: Introducción a Pandas y DataFrames
- 1.2.2: Limpieza de datos (nulos, tipos, columnas)
- 1.2.3: Transformaciones y generación de variables
- 1.2.4: Guardado de datos (CSV y Parquet)

### Capítulo 2 — Almacenamiento y consultas de datos
**Sección 3:** SQL y MySQL
- 2.3.1: Fundamentos SQL (SELECT, WHERE)
- 2.3.2: JOINs y agregaciones
- 2.3.3: Conexión Python → MySQL
- 2.3.4: Inserción y consulta del pipeline

**Sección 4:** Pipeline de datos v1
- 2.4.1: Integración CSV/API → transformación
- 2.4.2: Persistencia en MySQL y archivos
- 2.4.3: Modularización del pipeline
- 2.4.4: Ejecución completa del pipeline

### Capítulo 3 — Exposición y consumo de datos
**Sección 5:** APIs con FastAPI
- 3.5.1: Introducción a APIs y FastAPI
- 3.5.2: Endpoints básicos
- 3.5.3: Conexión API → base de datos
- 3.5.4: Filtros y validaciones

**Sección 6:** Visualización con Streamlit
- 3.6.1: Introducción a Streamlit
- 3.6.2: Dashboard básico
- 3.6.3: Conexión a API o datos procesados
- 3.6.4: Métricas y visualizaciones

### Capítulo 4 — Manejo de datos y despliegue local
**Sección 7:** Formatos de archivos y storage
- 4.7.1: CSV vs Parquet
- 4.7.2: Organización local de datos
- 4.7.3: Cloud storage (demo)
- 4.7.4: Integración con pipeline

**Sección 8:** Docker y entorno reproducible
- 4.8.1: Introducción a Docker
- 4.8.2: Creación de Dockerfile
- 4.8.3: requirements.txt y dependencias
- 4.8.4: docker-compose y servicios

### Capítulo 5 — Automatización y orquestación
**Sección 9:** Automatización de procesos
- 5.9.1: Scripts automatizados
- 5.9.2: Cronjobs
- 5.9.3: Logs y ejecución programada
- 5.9.4: Integración con pipeline

**Sección 10:** Orquestación e infraestructura
- 5.10.1: Introducción a Airflow
- 5.10.2: DAG simple
- 5.10.3: Infraestructura como código (demo)
- 5.10.4: Definición del proyecto final

### Capítulo 6 — Integración, despliegue y proyecto final
**Sección 11:** CI/CD y monitoreo
- 6.11.1: Introducción a GitHub y repositorios
- 6.11.2: CI/CD con GitHub Actions
- 6.11.3: Monitoreo (logs, health checks)
- 6.11.4: Seguimiento del proyecto

**Sección 12:** Presentación de proyecto e IA aplicada
- 6.12.1: Presentación de proyectos (parte 1)
- 6.12.2: Presentación de proyectos (parte 2)
- 6.12.3: IA como acelerador de ingeniería
