# PROMPT 2 — Generación de scripts y notebooks por capítulo
# Ejecutar después del Prompt 1
# Ejecutar una vez por capítulo: reemplaza [N] por 1, 2, 3, 4, 5 o 6

## CONTEXTO

Continuación del setup del curso "Python para Ingeniería de Datos" de BSG Institute.

El Prompt 1 ya creó la estructura del repo. Ahora debes:
1. Tomar los scripts `.py` existentes en `bsgfiles/` (los que ya tiene el instructor)
2. Moverlos a `scripts/cap[N]/` con el nombre correcto
3. Completar los scripts que falten para cubrir todos los bloques del capítulo
4. Convertir todos los scripts a notebooks `.ipynb` para Colab
5. Añadir la celda de instalación de dependencias a cada notebook

---

## VARIABLES — ajusta antes de ejecutar

```
CAPITULO = [N]          # número del capítulo a procesar (1-6)
```

---

## PASO 1 — Inventario de scripts existentes

Lee todos los archivos de `bsgfiles/` con nombre `[N]_*_Script.py`.
Encoding de lectura: `latin-1`.

Lista los que existen y los que faltan según el sílabo de referencia
(incluido al final de este prompt).

Ejemplo para capítulo 1, los archivos esperados son:
```
1_1_1_Script.py
1_1_2_Script.py
1_1_3_Script.py
1_1_4_Script.py
1_2_1_Script.py
1_2_2_Script.py
1_2_3_Script.py
1_2_4_Script.py
```

---

## PASO 2 — Copiar scripts existentes

Copia cada script existente de `bsgfiles/` a `scripts/cap[N]/`.
- Mantén el nombre exacto del archivo
- Encoding de lectura: `latin-1`
- Encoding de escritura: `utf-8`
- No modifiques el contenido original

---

## PASO 3 — Generar scripts faltantes

Para cada bloque del capítulo que NO tenga script, genera uno completo.

### Reglas de generación de scripts

**Encabezado obligatorio:**
```python
# ==============================================================================
# Capítulo [N]: [Nombre del capítulo]
# Sección [S]: [Nombre de la sección]
# Bloque [B]: [Nombre del bloque]
# ==============================================================================
# Subtemas cubiertos: [lista de STx del sílabo]
# Entorno: [Colab | Codespaces | Play with Docker]
# Prerequisito: [script anterior que debe correrse antes, o "Ninguno"]
# ==============================================================================
```

**Dataset del caso práctico** — todos los scripts usan estos campos:
```python
# Estructura estándar de una transacción del curso
transaccion = {
    "id_transaccion": "TXN-00001",   # str — identificador único
    "fecha": "2024-01-15",            # str — formato ISO YYYY-MM-DD
    "customer_id": 1001,              # int — ID numérico del cliente
    "amount": 250.50,                 # float — valor de la venta
    "status": "COMPLETADA",           # str — estado de la transacción
    "store": "CDMX-Norte"             # str — sucursal
}
```

**Estructura interna del script:**
- Separar en funciones nombradas por subtema (`ST1`, `ST2`, etc.)
- Comentarios en español explicando cada paso
- Bloque `if __name__ == "__main__":` que ejecuta el flujo completo
- Print statements claros que muestren qué está pasando
- Datos de ejemplo incluidos en el script (no depender de archivos externos,
  excepto cuando el bloque explícitamente lee un archivo generado antes)
- `random.seed(987654)` cuando se usen datos aleatorios

**Manejo de dependencias entre scripts:**
- Si el script necesita el CSV generado por `1_1_1_Script.py`,
  incluir una función `setup()` que lo genere si no existe
- Documentar claramente el prerequisito en el encabezado

**Entorno por capítulo/bloque:**
- Cap 1-3 y bloque 4.7.x → `# Entorno: Colab`
- Bloques 4.8.x (Docker) → `# Entorno: Play with Docker o Codespaces`
- Cap 5 (Airflow) → `# Entorno: Codespaces`
- Cap 6 → `# Entorno: Codespaces`

---

## PASO 4 — Convertir scripts a notebooks con jupytext

Para cada script en `scripts/cap[N]/`, genera el notebook correspondiente
en `notebooks/cap[N]/` usando jupytext:

```bash
jupytext --to notebook scripts/cap[N]/[archivo].py -o notebooks/cap[N]/[archivo].ipynb
```

Si jupytext no está instalado:
```bash
pip install jupytext --quiet
```

---

## PASO 5 — Añadir celda de setup a cada notebook

Después de convertir, abre cada `.ipynb` con Python y añade como
**primera celda** (tipo `code`) el siguiente contenido,
adaptado según el entorno del bloque:

### Para bloques Colab (Cap 1-3 y 4.7.x):
```python
# ============================================================
# 🚀 SETUP — Ejecuta esta celda primero
# ============================================================
# Instala las dependencias necesarias para este bloque

import sys

# Detectar si estamos en Colab
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    !pip install -r https://raw.githubusercontent.com/shanglai/bsg_python_data_engineering/main/requirements-colab.txt -q
    print("✅ Dependencias instaladas")
else:
    print("ℹ️  Ejecutando localmente — asegúrate de tener el entorno activo")

print(f"Python {sys.version}")
```

### Para bloques Codespaces (Cap 4.8.x, 5, 6):
```python
# ============================================================
# 🚀 SETUP — Lee esto antes de ejecutar
# ============================================================
# Este bloque requiere GitHub Codespaces o Docker instalado localmente.
#
# Si estás en Codespaces: el entorno ya está listo, puedes continuar.
# Si estás local: ejecuta primero `docker-compose up -d` en la terminal.
#
# ⚠️  Este notebook NO funciona en Google Colab.
# ============================================================

import sys
print(f"Python {sys.version}")
print("✅ Listo para comenzar")
```

### Para bloques Play with Docker (4.8.x demo):
```python
# ============================================================
# 🚀 SETUP — Play with Docker
# ============================================================
# Abre https://labs.play-with-docker.com/ en tu navegador
# Haz clic en "+ Add new instance"
# Copia y pega los comandos de cada celda en la terminal
# ============================================================
print("Abre https://labs.play-with-docker.com/ para continuar")
```

---

## PASO 6 — Añadir segunda celda de contexto a cada notebook

Añade como **segunda celda** (tipo `markdown`) en cada notebook:

```markdown
## 📍 Contexto del bloque

**Capítulo [N]:** [Nombre]
**Sección [S]:** [Nombre]
**Bloque [B]:** [Nombre]

**¿Qué vas a aprender?**
[3-4 bullets con los objetivos del bloque en lenguaje simple]

**¿Qué necesitas haber hecho antes?**
[Prerequisito o "Ninguno — este es el primer bloque"]

---
*BSG Institute · Python para Ingeniería de Datos · 2026*
```

---

## PASO 7 — Verificación

Al terminar, ejecuta:

```bash
# Listar scripts generados
ls -la scripts/cap[N]/

# Listar notebooks generados
ls -la notebooks/cap[N]/

# Verificar que todos los notebooks abren correctamente
python3 -c "
import json, os, glob
notebooks = glob.glob('notebooks/cap[N]/*.ipynb')
for nb in sorted(notebooks):
    with open(nb) as f:
        data = json.load(f)
    n_cells = len(data['cells'])
    print(f'OK: {os.path.basename(nb)} — {n_cells} celdas')
"
```

Reporta:
- Scripts copiados desde bsgfiles/
- Scripts generados nuevos
- Notebooks generados
- Errores de conversión o notebooks que no abrieron correctamente

---

## SÍLABO DE REFERENCIA — bloques esperados por capítulo

### Capítulo 1
- 1_1_1: Introducción al curso y caso del pipeline
- 1_1_2: Variables, tipos y estructuras básicas
- 1_1_3: Lectura de archivos CSV y primeros scripts
- 1_1_4: Funciones aplicadas a limpieza de datos
- 1_2_1: Introducción a Pandas y DataFrames
- 1_2_2: Limpieza de datos (nulos, tipos, columnas)
- 1_2_3: Transformaciones y generación de variables
- 1_2_4: Guardado de datos (CSV y Parquet)

### Capítulo 2
- 2_3_1: Fundamentos SQL (SELECT, WHERE)
- 2_3_2: JOINs y agregaciones
- 2_3_3: Conexión Python → MySQL
- 2_3_4: Inserción y consulta del pipeline
- 2_4_1: Integración CSV/API → transformación
- 2_4_2: Persistencia en MySQL y archivos
- 2_4_3: Modularización del pipeline
- 2_4_4: Ejecución completa del pipeline

### Capítulo 3
- 3_5_1: Introducción a APIs y FastAPI
- 3_5_2: Endpoints básicos
- 3_5_3: Conexión API → base de datos
- 3_5_4: Filtros y validaciones
- 3_6_1: Introducción a Streamlit
- 3_6_2: Dashboard básico
- 3_6_3: Conexión a API o datos procesados
- 3_6_4: Métricas y visualizaciones

### Capítulo 4
- 4_7_1: CSV vs Parquet
- 4_7_2: Organización local de datos
- 4_7_3: Cloud storage (demo — solo slides, sin script ejecutable)
- 4_7_4: Integración con pipeline
- 4_8_1: Introducción a Docker
- 4_8_2: Creación de Dockerfile
- 4_8_3: requirements.txt y dependencias
- 4_8_4: docker-compose y servicios

### Capítulo 5
- 5_9_1: Scripts automatizados
- 5_9_2: Cronjobs
- 5_9_3: Logs y ejecución programada
- 5_9_4: Integración con pipeline
- 5_10_1: Introducción a Airflow
- 5_10_2: DAG simple
- 5_10_3: Infraestructura como código (demo — solo slides)
- 5_10_4: Definición del proyecto final (sin script)

### Capítulo 6
- 6_11_1: Introducción a GitHub y repositorios
- 6_11_2: CI/CD con GitHub Actions
- 6_11_3: Monitoreo (logs, health checks)
- 6_11_4: Seguimiento del proyecto (sin script)
- 6_12_1: Presentación de proyectos parte 1 (sin script)
- 6_12_2: Presentación de proyectos parte 2 (sin script)
- 6_12_3: IA como acelerador de ingeniería
